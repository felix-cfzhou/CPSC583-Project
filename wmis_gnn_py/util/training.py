import argparse
import itertools
import pathlib

import torch
import torch_geometric as pyg
from tqdm import tqdm
import pandas as pd
import numpy as np

from arch.wmvc import WMVC
from util.parser import positive_integer, existing_directory, probability
from util.pyg_interface import WMISDataset


def make_training_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=existing_directory, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--output_name", type=str, required=True)
    parser.add_argument("--eval_size", type=probability, required=True)
    parser.add_argument("--batch_size", type=positive_integer, required=True)
    parser.add_argument("--num_epochs", type=positive_integer, required=True)
    parser.add_argument("--class1_weight", type=probability, required=True)
    parser.add_argument("--hidden_dim", type=positive_integer, required=True)
    parser.add_argument("--learning_rate", type=float, required=True)
    parser.add_argument("--momentum", type=probability, required=True)
    parser.add_argument("--max_dataset_len", type=positive_integer, required=True)
    parser.add_argument("--max_node_num", type=positive_integer, required=True)

    return parser


def train(model, data, optimizer, loss_fn):
    model.train()
    optimizer.zero_grad()
    y_pred = model(data.x, data.edge_index)
    loss = loss_fn(y_pred, data.solution.long().reshape(-1))
    loss.backward()
    optimizer.step()

    return loss.detach().cpu().numpy()


@torch.no_grad()
def test(model, data):
    model.eval()
    y_pred = torch.exp(model(data.x, data.edge_index))
    pred = y_pred.argmax(dim=1, keepdim=False)
    assert pred.shape == data.solution.shape
    acc = pred.eq(data.solution).float().mean().cpu()

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

    return acc.numpy(), np.mean(acc_10), np.mean(acc_1)


def main(args, model):
    dataset = WMISDataset(
        args.data_dir.resolve(),
        node_limit=args.max_node_num,
    ).shuffle()

    dataset_len = min(len(dataset), args.max_dataset_len)
    cutoff = int(dataset_len * args.eval_size)

    loader_train = pyg.loader.DataLoader(
        dataset[cutoff:dataset_len], batch_size=args.batch_size, shuffle=True
    )
    loader_eval = pyg.loader.DataLoader(
        dataset[:cutoff], batch_size=args.batch_size, shuffle=True
    )

    print(
        f"{dataset_len-cutoff} training graphs, {cutoff} eval graphs, at most {args.max_node_num} nodes each."
    )

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

    output_path = args.output_dir / args.output_name
    for epoch in tqdm(epochs, position=0, leave=True, desc="epoch"):
        train_loss_curr = 0.0
        train_acc_curr, train_acc_10_curr, train_acc_1_curr = 0.0, 0.0, 0.0
        for data in tqdm(loader_train, position=1, leave=False, desc="training batch"):
            loss = train(model, data.cuda(), optimizer, loss_fn)
            train_loss_curr += loss / len(loader_train)

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
        if not eval_acc_1 or (eval_acc_1_curr > max(eval_acc_1)):
            torch.save(
                model.state_dict(),
                output_path.with_stem(f"{output_path.stem}_epoch{epoch:05}").resolve(),
            )

            print(f"saving model from epoch {epoch} with eval acc_1: {eval_acc_1_curr}")
        elif not eval_acc_10 or (eval_acc_10_curr > max(eval_acc_10)):
            torch.save(
                model.state_dict(),
                output_path.with_stem(f"{output_path.stem}_epoch{epoch:05}").resolve(),
            )

            print(
                f"saving model from epoch {epoch} with eval acc_10: {eval_acc_10_curr}"
            )
        elif not eval_acc or (eval_acc_curr > max(eval_acc)):
            torch.save(
                model.state_dict(),
                output_path.with_stem(f"{output_path.stem}_epoch{epoch:05}").resolve(),
            )

            print(f"saving model from epoch {epoch} with eval acc: {eval_acc_curr}")
        elif epoch % 25 == 0:
            torch.save(
                model.state_dict(),
                output_path.with_stem(f"{output_path.stem}_epoch{epoch:05}").resolve(),
            )

            print(f"saving model from epoch {epoch} with eval acc: {eval_acc_curr}")

        train_loss.append(train_loss_curr)
        train_acc.append(train_acc_curr)
        train_acc_10.append(train_acc_10_curr)
        train_acc_1.append(train_acc_1_curr)
        eval_acc.append(eval_acc_curr)
        eval_acc_10.append(eval_acc_10_curr)
        eval_acc_1.append(eval_acc_1_curr)

        df = pd.DataFrame(
            {
                "train_loss": train_loss,
                "train_acc": train_acc,
                "train_acc_10": train_acc_10,
                "train_acc_1": train_acc_1,
                "eval_acc": eval_acc,
                "eval_acc_10": eval_acc_10,
                "eval_acc_1": eval_acc_1,
            }
        )
        df.to_csv(output_path.with_suffix(".csv").resolve(), index=False)

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

    torch.save(model.state_dict(), output_path.resolve())
