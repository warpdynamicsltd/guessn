from guessn.core import V, GF

class LogicFormula(GF):
  def __init__(self, model, *args):
    GF.__init__(self, model, *args)

  def __and__(self, other):
    return AND(self, other)
  
  def __or__(self, other):
    return OR(self, other)
  
  def __xor__(self, other):
    return XOR(self, other)
  
  def __invert__(self):
    return NOT(self)

class OR(LogicFormula):
  def __init__(self, *args):
    LogicFormula.__init__(self, lambda a, b: a or b, *args)

class XOR(LogicFormula):
  def __init__(self, *args):
    LogicFormula.__init__(self, lambda a, b: a != b, *args)


class AND(LogicFormula):
  def __init__(self, *args):
    LogicFormula.__init__(self, lambda a, b: a and b, *args)

class NOT(LogicFormula):
  def __init__(self, *args):
    LogicFormula.__init__(self, lambda a: not a, *args)
