import argparse
import fnmatch
import glob
import itertools
import os
import pathlib


def positive_integer(string):
  try:
    value = int(string)
    if value <= 0:
      raise Exception()
    
    return value
  except:
    raise argparse.ArgumentTypeError(f"{string} is not a positive integer!")

def existing_directory(string):
  path = pathlib.Path(string)
  if path.exists() and path.is_dir():
    return path

  raise argparse.ArgumentTypeError(f"{string} is not a directory!")

def existing_file(string):
  path = pathlib.Path(string)
  if path.exists() and path.is_file():
    return path

  raise argparse.ArgumentTypeError(f"{string} is not a file!")

def make_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument("graph_dirs", nargs='+', type=existing_directory, help="Directories to graphs in metis format. File names should end with .graph")
  parser.add_argument("--kamis", type=existing_file, required=True)
  parser.add_argument("--time_limit", type=positive_integer, required=True)
  parser.add_argument("--output_dir", type=existing_directory, required=True)

  return parser

def yield_graph_filenames(graph_dir):
  path = pathlib.Path(graph_dir)
  for filename in sorted(path.glob("*.graph")):
    yield filename

if __name__ == "__main__":
  parser = make_parser()
  args = parser.parse_args()

  for graph_filename in itertools.chain.from_iterable(yield_graph_filenames(graph_dir) for graph_dir in args.graph_dirs):
    output_filename = args.output_dir / graph_filename.with_suffix(".ind").name
    cmd_str = f"module load GCC; {args.kamis.resolve()} {graph_filename.resolve()} --time_limit={args.time_limit} --output={output_filename.resolve()}"
    print(cmd_str)
