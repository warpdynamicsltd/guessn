from guessn.core import GF
from guessn.themes.logic.simple_ascii import SimpleAsciiLogicTheme
from guessn.themes.theme import Theme
from guessn.models.arythmetic import Add, Sub, Mul, Divides
from guessn.models.logic import AND, OR, XOR, NOT

class SimpleAsciiTheme(SimpleAsciiLogicTheme):
  def repr_Divides(self, obj):
    return f"({self.repr(obj.args[0])} | {self.repr(obj.args[1])})"
  
  def repr_Add(self, obj):
    return f"({self.repr(obj.args[0])} + {self.repr(obj.args[1])})"
  
  def repr_Mul(self, obj):
    return f"({self.repr(obj.args[0])} * {self.repr(obj.args[1])})"
  


class SmartBracketsAsciiTheme(Theme):
  schemas = {
    Add: f"%s + %s",
    Sub: f"%s - %s",
    Mul: f"%s * %s",
    Divides: f"%s | %s",
    AND: f"%s and %s",
    OR: f"%s or %s",
    XOR: f"%s xor %s",
    NOT: f"~ %s"
  }

  priorities = {
    Mul: 10,
    Add: 9,
    Sub: 9,
    Divides: 8,
    NOT: 7,
    AND: 6,
    OR: 5,
    XOR: 5
  }

  def repr(self, obj):
    t = type(obj)
    if t in SmartBracketsAsciiTheme.schemas:
      priority = SmartBracketsAsciiTheme.priorities[t]
      args = []
      for arg in obj.args:
        t_ = type(arg)
        a = f"{self.repr(arg)}" if (not isinstance(arg, GF)) or (t_ in SmartBracketsAsciiTheme.priorities and SmartBracketsAsciiTheme.priorities[t_] > priority) else f"({self.repr(arg)})"   
        args.append(a)

      return SmartBracketsAsciiTheme.schemas[t] % tuple(args)
      
    else:
      return SimpleAsciiLogicTheme.repr(self, obj)