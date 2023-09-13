# Tetris AI

[Watch a trained model in action!](https://youtu.be/W_cV97VL5pE)

[Watch a model train from random to working](https://youtu.be/JFv-I273tug)

Uses a multi-layer linear model to predict the return for each possible action based on the resulting board state, then chooses the action with the highest predicted return. It is then trained at the end of each game based off of the the prediction for the board state of the action selected at each step compared to the actual return using Mean Squared Error. 

There is also a toggle to make the game human playable. Can you beat the high score of a trained model?

To predict the return, it takes the board state:
- Number of lines completed by the move
- Number of holes, empty blocks under a block occupied by a piece
- Bumpiness, sum of the height differences between adjacent columns
- Max height of any column

The model then outputs the predicted return for the action that results from that state. This approach was inspired by https://github.com/nuno-faria/tetris-ai

To calculate the possible states, it moves the current piece for each possible rotation and left/right movement, then drops the piece straight down. 

The discounted return takes into account the current return of the action plus a fraction of the score for each move after it. This is what is compared to the output of the model. The score itself is one point for each landed piece and 1000 points for each completed row. The one point per piece helps it train faster by trying to pack pieces more densely, which will also lead to completing rows. 

As the model gets more accurate at predicting discounted returns, selecting the highest predicted return also gets more accurate, leading to a better selection of action to increase future rewards.

## About this project
This has been my first foray into a machine learning project of my own. I had a great time writing my own version of Tetris using pygame and building my own machine learning model and training loop using pytorch. I was only able to get here because of the corses thanked below.

## Influenced by:
https://github.com/nuno-faria/tetris-ai

## Huge thanks to:
- Jeremy Howard and the fastai course (https://course.fast.ai/)
- Thomas Simonini, Omar Sanseviero, and the reinforcement learning course (https://huggingface.co/blog/deep-rl-intro)
