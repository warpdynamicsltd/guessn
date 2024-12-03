import random
import json
from itertools import permutations, product

from guessn.core import *
from guessn.models.gen import Gen
from guessn.models.logic import *


class State:
  def __init__(self, state, cat_index):
    self.state = state
    self.cat_index = cat_index
  
  def __eq__(self, other):
    self.state = other.state

  def __hash__(self):
    return hash(self.state)
  
  def __getitem__(self, cat):
    return self.state[self.cat_index[cat]]
  
  def __repr__(self):
    d = {}
    for cat in self.cat_index.keys():
      d[cat] = self[cat]

    return json.dumps(d)
  
def in_the_same_house(state, a, b):
  cat1, x1 = a
  cat2, x2 = b
  return state[cat1].index(x1) == state[cat2].index(x2)

def in_the_house_number(state, a, n):
  cat1, x1 = a
  return state[cat1].index(x1) == n
  
class SameHouse(LogicFormula):
  def __init__(self, *args):
    LogicFormula.__init__(self, in_the_same_house, *args)

class HouseNumber(LogicFormula):
  def __init__(self, *args):
    LogicFormula.__init__(self, in_the_house_number, *args)

class ZebraGen(Gen):
  categories = {
    "colors": ["red", "blue", "green", "yellow", "white", "black", "orange", "purple"],
    "pets": ["dog", "cat", "fish", "bird", "hamster", "turtle", "rabbit", "parrot"],
    "professions": ["teacher", "chef", "artist", "writer", "musician", "gardener", "scientist", "carpenter"],
    "furniture": ["sofa", "table", "chair", "bed", "bookshelf", "wardrobe", "desk", "cabinet"],
    "appliances": ["refrigerator", "oven", "microwave", "washing machine", "dishwasher", "vacuum cleaner", "fan", "air conditioner"],
    "decor": ["painting", "vase", "lamp", "clock", "rug", "curtains", "mirror", "cushion"],
    "hobbies": ["reading", "painting", "sewing", "knitting", "cooking", "playing board games", "playing guitar", "writing"]
  }

  representant = {
    "pets": "pets",
    "professions": "persons",
    "furniture": "furnitures",
    "appliances": "appliances",
    "decor": "items",
  }

  def __init__(self, n_categories=4, n_objects=4):
    self.n_categoris=n_categories
    self.n_objects=n_objects

    self.universe = {}
    cats = list(ZebraGen.categories.keys())
    cats.remove('professions')
    if n_categories >= 2:
      cats.remove('colors')
      self._categories = random.sample(cats, k=n_categories - 2)
      self._categories.append('colors')

    self._categories.append("professions")
   
    self._categories.sort()
    self.cat_index = {}

    for i, cat in enumerate(self._categories):
      self.universe[cat] = tuple(random.sample(ZebraGen.categories[cat], k=n_objects))
      self.cat_index[cat] = i

  def describe_puzzle(self, formulas):
    description = f"""
There are {self.n_objects} houses on a street with numbers from 1 to {self.n_objects}.
Each house is painted in a distinct color and the colors are: {', '.join(self.universe['colors'])}.
Only one person lives in each house and these people are: {', '.join(self.universe['professions'])}. 
"""
    
    if 'hobbies' in self.universe:
      description += f"Each of them has one of the following hobbies: {', '.join(self.universe['hobbies'])}" + '\n'
    
    for cat in self._categories:
      if cat not in ('colors', 'hobbies', 'professions'):
        description += f"There are {self.n_objects} {ZebraGen.representant[cat]}: {', '.join(self.universe[cat])} - one in each house." + '\n'

    description += '\n\n'

    for i, formula in enumerate(formulas):
      description += f"{i + 1}. {repr(formula).capitalize()}." + '\n'

    hobbies = ''
    if 'hobbies' in self.universe:
      hobbies = ' Also answer which hobby is whose.'

    description += f"""
Answer what are colors of houses and who lives at which address and what stuff is there.{hobbies}

Prepare response in a well formatted JSON like the following example:
{json.dumps(self.universe)}
"""

    return description

  def get_vars(self):
    return X_,

  def get_shuffled_universe(self):
    res = []
    for cat in self._categories:
      res.append(tuple(random.sample(self.universe[cat], k=self.n_objects)))

    return State(tuple(res), self.cat_index)

  def rnd_substitution(self):
    return {X_: self.get_shuffled_universe()}
  
  def model_generator(self):
    product_gen = product(*[permutations(self.universe[cat]) for cat in self._categories])
    return ((State(p, self.cat_index),) for p in product_gen)
  
  
  def rnd_same_house(self):
    cat1, cat2 = random.sample(self._categories, k=2)
    obj1 = random.choice(self.universe[cat1])
    obj2 = random.choice(self.universe[cat2])
    return SameHouse(X_, (cat1, obj1), (cat2, obj2))
  
  def rnd_house_number(self):
    cat = random.choice(self._categories)
    obj = random.choice(self.universe[cat])
    n = random.randint(0, self.n_objects - 1)
    return HouseNumber(X_, (cat, obj), n)
  
  def rnd_atomic_formula(self):
    method = random.choice([self.rnd_same_house, self.rnd_house_number])
    return method()
  
  def rnd_formula(self):
    f1 = self.rnd_atomic_formula()
    if bool(random.choice([0, 1])):
      return f1
    
    f2 = self.rnd_atomic_formula()
    #return random.choice([f1, f2])
    return f1 | f2


      




  
