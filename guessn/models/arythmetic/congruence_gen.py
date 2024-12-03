import random
import math
from collections import defaultdict
from itertools import product
from operator import and_
from functools import reduce

from guessn.core import *
from guessn.models.arythmetic import Add, Sub, Mul, Divides
from guessn.models.gen import Gen

class CongruenceGen(Gen):
  term_consts = [1, 2, 3, 4, 5]
  special_vars = [A_, B_, C_, D_, E_]
  
  def __init__(self, _min, _max, n_vars):
    self.min = _min
    self.max = _max
    self.n_vars = n_vars

    self.vars_ = [V(f'V{i}') for i in range(self.n_vars)]
    self.vars =  CongruenceGen.special_vars[:self.n_vars] + self.vars_[:max(0, self.n_vars - len(CongruenceGen.special_vars))]

  def get_vars(self):
    return self.vars

  def rnd_div_form(self, vars):
    op = random.choice([Add, Sub])
    if bool(random.choice([0, 1])):
      t = op(random.choice(CongruenceGen.term_consts), random.choice(vars))
    else:
      t = op(vars[0], vars[1])

    return Divides(random.randint(2, int(math.sqrt(self.max))), t)

  def rnd_divs(self, n):
    res = []
    for _ in range(n):
      f1 = self.rnd_div_form(random.sample(self.vars, k=2))
      f2 = self.rnd_div_form(random.sample(self.vars, k=2))
      
      op = bool(random.choice([0, 1, 1, 1, 1, 1]))

      if op:
        res.append(f1 & f2)
      else:
        res.append(f1 | f2)

    return res
  
  def rnd_formulas(self, n, substitution):
    res = []
    while len(res) < n:
      f, = self.rnd_divs(1)
      if f(substitution):
        res.append(f)
  
    return res
  
  def rnd_substitution(self):
    substitution = {}
    for var in self.vars:
      substitution[var] = random.randint(self.min, self.max)
    return substitution
  
  def model_generator(self):
    return product(range(self.min, self.max + 1), repeat=self.n_vars)
