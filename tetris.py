#! /usr/bin/env python3

import pygame

import cv2

import time
from datetime import datetime

import colors
from moves import Moves

from tetris_env import TetrisEnv

from model import TetrisModel

import numpy as np

import torch
import torch.optim as optim
import torch.nn.functional as F

from collections import deque

import random

debug = False

human = False
gui = human or True
record = False
record_first_games = 500

# save_best and load_best are mutually exclusive
save_best = True
load_best = False
best_model_path = "tetris_model.pt"

clock_speed = 0.2
background_color = colors.BLACK

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

scores_deque = deque(maxlen=100)

hyperparameters = {
    "h_size": 32,
    "h_layers": 2,
    "gamma": 0.999,
    "lr": 1e-2,
    "bs": 50,
    "clamp_reward_percentile": None,
    "state_space": 4
}

randomize_batches = True

print_every = 100

policy = TetrisModel(hyperparameters["state_space"], hyperparameters["h_size"], hyperparameters["h_layers"]).to(device)
optimizer = optim.Adam(policy.parameters(), lr=hyperparameters["lr"])

if load_best:
  policy.load_state_dict(torch.load(best_model_path))

env = TetrisEnv()
 
pygame.init()

window_width = 750
window_height = 600
 
surface = pygame.display.set_mode((window_width, window_height))
if record:
  video_writer = cv2.VideoWriter("tetris.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 150, (window_width, window_height))
font = pygame.font.Font(pygame.font.get_default_font(), 36)

env.reset()
saved_state_stats = []
rewards = []

all_rewards = torch.tensor([]).to(device)

running = True
high_score = 0
tries = 0
recent_scores = []
start_time = datetime.now()

def render(debug, record, background_color, env, surface, font, high_score, tries, recent_scores, start_time):
    surface.fill(background_color)

    env.board.render(surface)

    text_offset = 300

    text_surface = font.render(f"Score: {env.score}", True, (255, 255, 255))
    surface.blit(text_surface, dest=(text_offset, 50))
    text_surface = font.render(f"Time: {datetime.now() - start_time}", True, (255, 255, 255))
    surface.blit(text_surface, dest=(text_offset, 100))

    if env.score > high_score:
      high_score = env.score
    text_surface = font.render(f"High score: {high_score}", True, (255, 255, 255))
    surface.blit(text_surface, dest=(text_offset, 150))

    text_surface = font.render(f"Tries: {tries}", True, (255, 255, 255))
    surface.blit(text_surface, dest=(text_offset, 200))

    recent_scores = recent_scores[-100:]
    if len(recent_scores) > 0:
      text_surface = font.render(
          f"Rolling average: {int(sum(recent_scores) / len(recent_scores))}", 
          True, 
          (255, 255, 255)
        )
      surface.blit(text_surface, dest=(text_offset, 250))

    if record:
      frame = pygame.display.get_surface()
      view = pygame.surfarray.array3d(frame)
      view = view.transpose([1, 0, 2])
      image = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
      video_writer.write(image)

    pygame.display.flip()

      ## show possible states
    if debug:
      for possible_state in env.get_possible_states():
        surface.fill(background_color)
        text_surface = font.render(f"State stats: {possible_state[0].get_stats()}", True, (255, 255, 255))
        surface.blit(text_surface, dest=(text_offset, 50))
        possible_state[0].render(surface)
        pygame.display.flip()
        time.sleep(0.1)
      surface.fill(background_color)
      env.board.render(surface)
      pygame.display.flip()
      time.sleep(0.5)
    return high_score,recent_scores

try:
  # main loop
  while running:
    action = None
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if human and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
          action = Moves.RIGHT
        if event.key == pygame.K_LEFT:
          action = Moves.LEFT
        if event.key == pygame.K_UP:
          action = Moves.ROTATE
        if event.key == pygame.K_DOWN:
          action = Moves.DROP
      
    if not human:
      predicted_scores = []
      all_state_stats = []
      actions = []

      for state in env.get_possible_states():
        state_stats = state[0].get_stats()
        state_stats = torch.tensor(state_stats).float().to(device)

        all_state_stats.append(state_stats)
        actions.append(state[1])

      # don't update gradients until we pick the best action
      with torch.no_grad():
        predicted_scores = policy(torch.stack(all_state_stats).to(device))
        predicted_scores = predicted_scores.flatten().tolist()

      index = predicted_scores.index(max(predicted_scores))
      saved_state_stats.append(all_state_stats[index])
    
      action = actions[index]

    # take action with highest predicted score
    reward, done = env.step(action)
    rewards.append(reward)

    # save model if it's the best so far before updating
    if save_best and env.score > high_score and not human and not load_best:
      torch.save(policy.state_dict(), best_model_path)
    
    if gui:
      high_score, recent_scores = render(debug, record, background_color, env, surface, font, high_score, tries, recent_scores, start_time)

    if env.board.game_over:
      if not human and not load_best:
        scores_deque.append(sum(rewards))

        returns = deque()
        n_steps = len(rewards)

        # calculate discounted returns going backwards
        for t in range(n_steps - 1, -1, -1):
          disc_return_t = (returns[0] if len(returns)>0 else 0)
          return_t = hyperparameters["gamma"]*disc_return_t + rewards[t]
          return_t = torch.tensor([return_t], requires_grad=True).to(device)
          returns.appendleft(return_t)

        # randomize saved state stats and return pairs for more diverse batches
        if randomize_batches:
          zipped = list(zip(saved_state_stats, returns))
          random.shuffle(zipped)
          saved_state_stats, returns = zip(*zipped)
        
        # convert returns to tensor
        returns = torch.tensor(returns, requires_grad=False).to(device)

        # Clamp rewards to Nth percentile to reduce the influence of outliers so the model doesn't blow up
        all_rewards = torch.cat([all_rewards, returns])
        if hyperparameters["clamp_reward_percentile"] and hyperparameters["clamp_reward_percentile"] > 0:
          top = max(torch.quantile(all_rewards, hyperparameters["clamp_reward_percentile"]), 5_000)   # Make sure it has room to learn about rows
          returns = torch.clamp(returns, 0, top)

        returns = returns[:, None]

        # update policy using mean squared error loss of predicted score vs. discounted return
        for i in range(0, len(saved_state_stats), hyperparameters["bs"]):
          batch_start = i
          batch_end = i + hyperparameters["bs"]
          if batch_end > len(saved_state_stats):
            batch_end = len(saved_state_stats)

          batch_stats = torch.stack(saved_state_stats[batch_start:batch_end]).to(device)

          # calculate loss
          loss = F.mse_loss(policy(batch_stats), returns[batch_start:batch_end])

          loss.backward()
          optimizer.step()
          optimizer.zero_grad()

        if tries % print_every == 0:
          print('Episode {}\tAverage Score: {:.2f}'.format(tries, np.mean(scores_deque)))
          print(f"High score: {high_score}")

      saved_state_stats = []
      rewards = []
      recent_scores.append(env.score)
      start_time = datetime.now()
      env.reset()
      tries += 1

      if record and record_first_games and record_first_games > 0 and tries > record_first_games:
        video_writer.release()
        record = False

    if human:
      time.sleep(clock_speed)

  if record:
    video_writer.release()
  pygame.quit()
except SystemExit:
  pygame.quit()
