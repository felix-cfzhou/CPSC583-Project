import argparse
import itertools
import pathlib

import torch
import torch_geometric as pyg
from tqdm import tqdm
import numpy as np

from arch.wmvc import WMVC
from util.parser import positive_integer, existing_directory, probability
from util.pyg_interface import WMISDataset


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=existing_directory, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--output_name", type=str, required=True)
    parser.add_argument("--eval_size", type=probability, required=True)
    parser.add_argument("--batch_size", type=positive_integer, required=True)
    parser.add_argument("--num_epochs", type=positive_integer, required=True)
    parser.add_argument("--class1_weight", type=probability, required=True)
    parser.add_argument("--hidden_layers", type=positive_integer, required=True)
    parser.add_argument("--learning_rate", type=float, required=True)
    parser.add_argument("--momentum", type=probability, required=True)

    return parser


def train(model, training_set, optimizer, loss_fn):
    loss = 0

    model.train()
    optimizer.zero_grad()
    y_pred = model(data.x, data.edge_index)
    loss = loss_fn(y_pred, data.solution.long().reshape(-1))
    loss.backward()
    optimizer.step()

    return loss.cpu()


@torch.no_grad()
def test(model, data):
    model.eval()
    y_pred = torch.exp(model(data.x, data.edge_index))
    pred = y_pred.argmax(dim=1, keepdim=False)
    assert pred.shape == data.solution.shape
    acc = pred.eq(data.solution).float().mean()

    batch_ids = torch.unique(data.batch)
    acc_10, acc_1 = [], []
    for batch_id in batch_ids:
        y_pred_batch_sorted, indices = y_pred[data.batch == batch_id].sort(
            dim=0, descending=True
        )
        # print(y_pred_batch_sorted)
        solution_batch = data.solution[data.batch == batch_id]
        # print(solution_batch)
        acc_10.append(solution_batch[indices[:10, 1]].eq(1).float().mean().cpu())
        acc_1.append(solution_batch[indices[0, 1]].eq(1).float().cpu())

    return acc.cpu(), np.mean(acc_10), np.mean(acc_1)


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    dataset = WMISDataset(
        args.data_dir.resolve(),
        transform=pyg.transforms.AddLaplacianEigenvectorPE(
            k=2, attr_name=None, is_undirected=True
        ),
    ).shuffle()

    cutoff = int(len(dataset) * args.eval_size)

    loader_train = pyg.loader.DataLoader(dataset[cutoff:], batch_size=64, shuffle=True)
    loader_eval = pyg.loader.DataLoader(dataset[:cutoff], batch_size=64, shuffle=True)

    model = WMVC(5, args.hidden_layers, 2).cuda()

    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=args.learning_rate,
        momentum=args.momentum,
        # nesterov=True,
    )

    class_weight = weight = torch.Tensor(
        [1 - args.class1_weight, args.class1_weight]
    ).cuda()
    loss_fn = torch.nn.NLLLoss(weight=class_weight)

    epochs = list(range(1, args.num_epochs + 1))
    (
        train_loss,
        train_acc,
        train_acc_10,
        train_acc_1,
        eval_acc,
        eval_acc_10,
        eval_acc_1,
    ) = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )

    # best_eval_acc = float("-inf")
    for epoch in tqdm(epochs, position=0, leave=True, desc="epoch"):
        train_loss_curr = 0.0
        train_acc_curr, train_acc_10_curr, train_acc_1_curr = 0.0, 0.0, 0.0
        for data in tqdm(loader_train, position=1, leave=False, desc="training batch"):
            loss = train(model, data.cuda(), optimizer, loss_fn).detach()
            train_loss_curr += loss / len(loader_train)

        for data in tqdm(loader_train, position=1, leave=False, desc="training eval"):
            acc, acc_10, acc_1 = test(model, data.cuda())
            train_acc_curr += acc / len(loader_train)
            train_acc_10_curr += acc_10 / len(loader_train)
            train_acc_1_curr += acc_1 / len(loader_train)

        eval_acc_curr, eval_acc_10_curr, eval_acc_1_curr = 0.0, 0.0, 0.0
        for data in tqdm(loader_eval, position=1, leave=False, desc="eval batch"):
            acc, acc_10, acc_1 = test(model, data.cuda())
            eval_acc_curr += acc / len(loader_eval)
            eval_acc_10_curr += acc_10 / len(loader_eval)
            eval_acc_1_curr += acc_1 / len(loader_eval)

        # scheduler.step(eval_acc_10_curr)

        train_loss.append(train_loss_curr)
        train_acc.append(train_acc_curr)
        train_acc_10.append(train_acc_10_curr)
        train_acc_1.append(train_acc_1_curr)
        eval_acc.append(eval_acc_curr)
        eval_acc_10.append(eval_acc_10_curr)
        eval_acc_1.append(eval_acc_1_curr)

        if epoch % 5 == 0:
            if eval_acc_1_curr > max(eval_acc_1[:-1]):
                output_path = args.output_dir / f"{args.output_name}.epoch{epoch:05}"
                torch.save(model, output_path.resolve())

            print(f"After epoch {epoch}:")
            print(
                f"train acc: {train_acc_curr}, train acc_10: {train_acc_10_curr}, train acc_1: {train_acc_1_curr},"
            )
            print(
                f"eval acc: {eval_acc_curr}, eval acc_10: {eval_acc_10_curr}, eval acc_1: {eval_acc_1_curr}"
            )
            print(
                "----------------------------------------------------------------------------------------"
            )

    output_path = args.output_dir / args.output_name
    torch.save(model, output_path.resolve())
