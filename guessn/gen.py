import random
import math
from guessn.builtin import add, sub, mul, divides
from guessn.core import LogicFormula

from collections import defaultdict
from itertools import product
from operator import and_
from functools import reduce

term_consts = [1, 2, 3, 4, 5]
divides_consts = [2, 3, 5, 7, 11, 13]

def rnd_term():
  consts = term_consts
  atoms = [add, sub]
  op = random.choice(atoms)
  A = op.substitute({'A': random.choice(consts), 'B':'X'})
  factor = random.choice(consts)
  B = mul.substitute({'A': factor, 'B': A})
  op = random.choice(atoms)
  return factor, op.substitute({'A': B, 'B': random.choice(consts)})


def rnd_predicates(n):
  res = []
  for k in range(n):
    p = divides_consts[k]
    
    while True:
      factor, t = rnd_term()
      if p != factor:
        break

    res.append(divides.substitute({'B': t, 'A': p}))

  return res

def rnd_div(vars, limit):
  op = random.choice([add, sub])
  if bool(random.choice([0, 1])):
    t = op.substitute({'B': random.choice(term_consts), 'A':random.choice(vars)})
  else:
    t = op.substitute({'B': vars[0], 'A':vars[1]})


  #return LogicFormula(args=[divides.substitute({'B': t, 'A': rnd_cmp(limit)})])
  return LogicFormula(args=[divides.substitute({'B': t, 'A': random.randint(2, int(math.sqrt(limit)))})])

def rnd_divs(vars, limit, n):
  res = []
  for _ in range(n):
    f1 = rnd_div(random.sample(vars, k=2), limit)
    f2 = rnd_div(random.sample(vars, k=2), limit)
    #f3 = rnd_div(used_vars[2], limit)
    op = bool(random.choice([0, 1, 1, 1, 1, 1]))
    # neg = bool(random.randint(0, 1))
    neg = False
    if neg:
        f2 = ~f2

    # print(f1, f2)
    if op:
      res.append(f1 & f2)
    else:
      res.append(f1 | f2)

  return res


def rnd_divs_const(vars, limit, n, substitution):
  res = []
  while len(res) < n:
    f, = rnd_divs(vars, limit, 1)
    if f(substitution):
      res.append(f)
  
  return res


def rnd_cmp(limit):
  consts = list(divides_consts)
  random.shuffle(consts)

  res = 1
  
  for c in consts:
    for _ in range(3):
      p = random.randint(1, 3)
      res_ = res * (c ** p)
      if res_ > limit:
        continue
      res = res_
      break

  return res


class PuzzleGen:
  def __init__(self, _min, _max, max_n_formulas=20):
    self._min = _min
    self._max = _max
    self.max_n_formulas = max_n_formulas
  
  def gen_candidates_formulas(self):
    substitution = {'X': random.randint(self._min, self._max), 'Y': random.randint(self._min, self._max), 'Z': random.randint(self._min, self._max)}
    formulas = rnd_divs_const(['X', 'Y', 'Z'], self._max, self.max_n_formulas, substitution)

    return formulas, substitution
  
  def create_sets(self, formulas):
    sets = defaultdict(set)
    res = []

    for x, y, z in product(range(self._min, self._max + 1), range(self._min, self._max + 1), range(self._min, self._max + 1)):
      success = True
      for i, f in enumerate(formulas):
        if not f({'X': x, 'Y': y, 'Z': z}):
          success = False
        else:
          sets[i].add((x, y, z))

      if success:
        res.append((x, y, z))

    if len(res) == 1:
      return sets

    return None
  
  def eliminate_one(self, sets):
    for candidate in sets.keys():
      l = list(sets.keys())
      l.remove(candidate)
      res = reduce(and_, map(lambda k: sets[k], l))
      if len(res) == 1:
        return candidate
      
    return -1
  
  def gen_formulas(self, attemps=10):
    sets = None
    formulas = None
    substitution = None
    for _ in range(attemps):
      formulas, substitution = self.gen_candidates_formulas()
      sets = self.create_sets(formulas)
      if sets is not None:
        break
    if sets is None:
      return None, None
    
    while True:
      index = self.eliminate_one(sets)
      if index == -1:
        break
      del sets[index]

    return [formulas[k] for k in sets.keys()], substitution
    
    

  

  


  

  






