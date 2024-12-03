class V:
  def __init__(self, name):
    self.name = name

  def __eq__(self, other):
    return type(other) is type(self) and hasattr(other, 'name') and self.name == other.name
  
  def __hash__(self):
    return hash(self.name)
  
  def __repr__(self):
    return self.name
  

A_ = V('A')
B_ = V('B')
C_ = V('C')
D_ = V('D')
E_ = V('E')
X_ = V('X')
Y_ = V('Y')
Z_ = V('Z')

class DefaultTheme:
  def repr(self, obj):
    if isinstance(obj, GF):
      return f"{type(obj).__name__}({', '.join(map(lambda a: self.repr(a), obj.args))})"
    else:
      return repr(obj)

class GF:
  default_theme = DefaultTheme()

  def __init__(self, model, *args):
    self.model = model
    self.args = args

  def __call__(self, substitution):
    values = []
    for arg in self.args:
      if isinstance(arg, V):
        v = substitution[arg]
      elif isinstance(arg, GF):
        v = arg(substitution)
      else:
        v = arg

      values.append(v)

    return self.model(*values)
  
  def substitute(self, substitution):
    substituted_args = []
    for arg in self.args:
      if isinstance(arg, V) and arg in substitution:
        substituted_args.append(substitution[arg])
      elif isinstance(arg, GF):
        substituted_args.append(arg.substitute(substitution))
      else:
        substituted_args.append(arg)

    return type(self)(*substituted_args)
  
  def __repr__(self):
    return GF.default_theme.repr(self)

  

class Term(GF):
  pass