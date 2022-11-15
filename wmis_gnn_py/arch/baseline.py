import torch
import torch_geometric as pyg

from arch.mlp import MLP


class Baseline(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()

        self.conv1 = pyg.nn.LGConv(normalize=False)
        self.mlp1 = MLP(-1, hidden_channels, hidden_channels // 2)
        self.conv2 = pyg.nn.LGConv(normalize=False)
        self.mlp2 = MLP(-1, hidden_channels, hidden_channels // 2)
        self.conv3 = pyg.nn.LGConv(normalize=False)
        self.mlp3 = MLP(-1, hidden_channels, out_channels)
        self.log_softmax = torch.nn.LogSoftmax(dim=1)

    def forward(self, node_feature, edge_index):
        result_conv1 = self.conv1(node_feature, edge_index)
        result_concat1 = torch.concat([result_conv1, node_feature], dim=1)
        result_mlp1 = self.mlp1(result_concat1)
        result_act1 = torch.relu(result_mlp1)

        result_conv2 = self.conv2(result_act1, edge_index)
        result_concat2 = torch.concat([result_conv2, result_act1, node_feature], dim=1)
        result_mlp2 = self.mlp2(result_concat2)
        result_act2 = torch.relu(result_mlp2)

        result_conv3 = self.conv3(result_act2, edge_index)
        result_concat3 = torch.concat([result_conv3, result_act2, node_feature], dim=1)
        result_mlp3 = self.mlp3(result_concat3)

        output = self.log_softmax(result_mlp3)

        return output
