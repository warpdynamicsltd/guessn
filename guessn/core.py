class Term:
  def __init__(self, function=lambda a:a, op_name='id', repr='%s', args=[]):
    self.function = function
    self.op_name = op_name
    self.args = args
    self.repr = repr

  def __call__(self, substitution):
    values = []
    for arg in self.args:
        if isinstance(arg, str):
          v = substitution[arg]
        elif isinstance(arg, Term):
          v = arg(substitution)
        else:
          v = arg

        values.append(v)

    return self.function(*values)
  
  def substitute(self, substitution):
    values = []
    for arg in self.args:
        if isinstance(arg, str):
          v = substitution[arg]
        else:
          v = arg

        values.append(v)
    return Term(self.function, self.op_name, self.repr, values)
  

  def __repr__(self):
    args = [f'({arg})' if isinstance(arg, Term) and arg.op_name != '*' else str(arg) for arg in self.args]
    return self.repr % tuple(args)



class Predicate:
  def __init__(self, function, repr, args):
    self.function = function
    self.args = args
    self.repr = repr

  def __call__(self, substitution):
    values = []
    for arg in self.args:
        if isinstance(arg, str):
          v = substitution[arg]
        elif isinstance(arg, Term):
          v = arg(substitution)
        else:
          v = arg

        values.append(v)

    return self.function(*values)
  
  def substitute(self, substitution):
    values = []
    for arg in self.args:
        if isinstance(arg, str):
          v = substitution[arg]
        else:
          v = arg

        values.append(v)
    return Predicate(self.function, self.repr, values)
  
  def __repr__(self):
    return self.repr % tuple(self.args)


class LogicFormula:
  def __init__(self, op=lambda a:a, op_name='id', args=[]):
    self.op = op
    self.op_name = op_name
    self.args = args

  def __call__(self, substitution):
    values = [arg(substitution) for arg in self.args]
    return self.op(*values) 
  
  def __invert__(self):
    return LogicFormula(lambda a:not a, 'not', args=[self])
  
  def __or__(self, formula):
    return LogicFormula(lambda a, b: a or b, 'or', args=[self, formula])
  
  def __and__(self, formula):
    return LogicFormula(lambda a, b: a and b, 'and', args=[self, formula])
  
  def __xor__(self, formula):
    return LogicFormula(lambda a, b: a != b, 'xor', args=[self, formula])
  
  def __repr__(self):
    if self.op_name == 'id':
      return repr(self.args[0])
    
    if self.op_name == 'not':
      return f'it is not true that {self.args[0]}'
    
    if self.op_name == 'or':
      return f'{self.args[0]} or {self.args[1]}'
    
    if self.op_name == 'and':
      return f'{self.args[0]} and {self.args[1]}'

    if self.op_name == 'xor':
      return f'{self.args[0]} or {repr(self.args[1])} but not both' 
    
    return 'UNKNOWN'
    

                


    
