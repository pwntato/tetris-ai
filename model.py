
import torch.nn as nn
import torch.nn.functional as F

class TetrisModel(nn.Module):
  def __init__(self, s_size, h_size, h_layers):
    super(TetrisModel, self).__init__()

    layers = [
      nn.Linear(s_size, h_size), 
      nn.ReLU()
    ]

    for _ in range(h_layers):
      layers.append(nn.Linear(h_size, h_size))
      layers.append(nn.ReLU())
    
    layers.append(nn.Linear(h_size, 1))

    self.layers = nn.Sequential(*layers)

  def forward(self, x):
    return self.layers(x)
  