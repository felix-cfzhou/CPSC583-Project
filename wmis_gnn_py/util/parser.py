import argparse
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

