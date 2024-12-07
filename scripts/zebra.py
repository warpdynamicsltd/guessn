import time
from guessn.core import *
from guessn.themes.zebra.simple_zebra import SimpleZebraTheme
from guessn.models.zebra import ZebraGen

GF.default_theme = SimpleZebraTheme()

def main():
  puzzle_gen = ZebraGen()

  start = time.time()
  formulas, substitution = puzzle_gen.gen_formulas(max_n_formulas=20)
  print(f"puzzle create in {time.time() - start:.2f} sec")

  print(puzzle_gen.describe_puzzle(formulas))
  print("***")
  print(substitution)



if __name__ == "__main__":
  main()