from guessn.themes.theme import Theme

class SimpleAsciiLogicTheme(Theme):
  def repr_OR(self, obj):
    return f"({self.repr(obj.args[0])} or {self.repr(obj.args[1])})"

  def repr_XOR(self, obj):
    return f"({self.repr(obj.args[0])} xor {self.repr(obj.args[1])})"  
  
  def repr_AND(self, obj):
    return f"({self.repr(obj.args[0])} and {self.repr(obj.args[1])})"

  def repr_NOT(self, obj):
    return f"(~{self.repr(obj.args[0])})" 
