from guessn.core import GF

class Theme:
  def repr(self, obj):
    try:
      method = getattr(self, f'repr_{type(obj).__name__}')
    except AttributeError:
      method = self.repr_default

    return method(obj)

  def repr_V(self, obj):
    return f"{obj.name}"

  def repr_default(self, obj):
    if isinstance(obj, GF):
      return f"{type(obj).__name__}({', '.join(map(lambda a: self.repr(a), obj.args))})"
    else:
      return repr(obj)