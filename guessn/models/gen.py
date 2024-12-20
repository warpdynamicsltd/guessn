from collections import defaultdict
from itertools import product
from operator import and_
from functools import reduce
from abc import ABC, abstractmethod

class Gen(ABC):
  @abstractmethod
  def rnd_formula(self):
    pass
  
  @abstractmethod
  def rnd_substitution(self):
    pass
  
  @abstractmethod
  def model_generator(self):
    pass

  @abstractmethod
  def get_vars(self):
    pass

  def rnd_formulas(self, n, substitution):
    res = []
    while len(res) < n:
      f = self.rnd_formula()
      if f(substitution):
        res.append(f)
  
    return res

  def gen_candidates_formulas(self, max_n_formulas):
    substitution = self.rnd_substitution()
    formulas = self.rnd_formulas(max_n_formulas, substitution)
    return formulas, substitution
  
  def create_sets(self, formulas):
    vars = self.get_vars()
    sets = defaultdict(set)
    res = []

    for vector in self.model_generator():
      success = True
      for k, f in enumerate(formulas):
        if not f({vars[i]:vector[i] for i, _ in enumerate(vars)}):
          success = False
        else:
          sets[k].add(hash(vector))

      if success:
        res.append(hash(vector))

    return len(res), sets
  
  def eliminate_one(self, sets):
    for candidate in sets.keys():
      l = list(sets.keys())
      l.remove(candidate)
      res = reduce(and_, map(lambda k: sets[k], l))
      if len(res) == 1:
        return candidate
      
    return -1
  
  def gen_formulas(self, max_n_formulas=20, attemps=10):
    sets = None
    formulas = None
    substitution = None
    for _ in range(attemps):
      formulas, substitution = self.gen_candidates_formulas(max_n_formulas)
      solutions, sets = self.create_sets(formulas)
      if solutions == 1:
        break
    if solutions > 1:
      return None, None
    
    while True:
      index = self.eliminate_one(sets)
      # print(len(sets))
      if index == -1:
        break
      del sets[index]

    return [formulas[k] for k in sets.keys()], substitution
  
