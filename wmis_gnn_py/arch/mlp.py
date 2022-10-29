import torch
import torch_geometric as pyg


class MLP(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()

        self.in_channels = in_channels
        self.hidden_channels = hidden_channels
        self.out_channels = out_channels

        self.sequential = torch.nn.Sequential(
            pyg.nn.Linear(in_channels, hidden_channels),
            torch.nn.Dropout(p=0.2),
            torch.nn.ReLU(),
            pyg.nn.Linear(hidden_channels, hidden_channels),
            torch.nn.Dropout(p=0.2),
            torch.nn.ReLU(),
            pyg.nn.Linear(hidden_channels, out_channels),
            torch.nn.Dropout(p=0.2),
        )

    def forward(self, x):

        batch_size = x.shape[0]
        x = x.view(batch_size, -1)  # reshape the tensor to a 1-D vector

        out = self.sequential(x)

        return out
