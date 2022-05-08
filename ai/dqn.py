import torch.nn as nn

#TODO: make ai agent

class DQN(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super().__init()
        self.fc1 == nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return self.fc1(x)
