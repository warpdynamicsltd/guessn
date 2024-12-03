from guessn.core import V, Term
from guessn.models.logic import LogicFormula

class Divides(LogicFormula):
  def __init__(self, *args):
    LogicFormula.__init__(self, lambda a, b: b % a == 0, *args)

class Add(Term):
  def __init__(self, *args):
    Term.__init__(self, lambda a, b: a + b, *args)

class Sub(Term):
  def __init__(self, *args):
    Term.__init__(self, lambda a, b: a - b, *args)

class Mul(Term):
  def __init__(self, *args):
    Term.__init__(self, lambda a, b: a * b, *args)