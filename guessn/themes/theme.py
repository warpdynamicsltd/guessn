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
    return repr(obj)