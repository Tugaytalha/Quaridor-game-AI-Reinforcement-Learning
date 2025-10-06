import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os


class quoridorGo(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
