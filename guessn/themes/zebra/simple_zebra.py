from guessn.themes.theme import Theme

def article(a):
  if a[0] in ('a', 'e', 'u', 'o', 'i', 'h'):
    return "an"
  else:
    return "a"

schema = {
  ('colors', 'pets'): lambda a, b: f"a {b} lives in {article(a)} {a} house",
  ('colors', 'professions'): lambda a, b: f"{article(b)} {b} lives in {article(a)} {a} house",
  ('colors', 'hobbies'): lambda a, b: f"a person who lives in {article(a)} {a} house is {b}",
  ('colors', '*'): lambda a, b: f"there is {article(b)} {b} in {article(a)} {a} house",
  ('professions', 'hobbies'): lambda a, b: f"{article(a)} {a} is {b}",
  ('professions', 'pets'): lambda a, b: f"{article(a)} {a} has {article(b)} {b}",
  ('professions', '*'): lambda a, b: f"{article(a)} {a} has {article(b)} {b}",
  ('pets', '*'): lambda a, b: f"{article(a)} {a} lives in a house with {article(b)} {b}",
  ('hobbies', 'pets'): lambda a, b: f"a person who is {a} has {article(b)} {b}",
  ('hobbies', '*'): lambda a, b: f"an owner of {article(b)} {b} is {a}",
  ('*', '*'): lambda a, b: f"an owner of {article(a)} {a} has {article(b)} {b}"
}

neighbour_schema = {
  ('colors', 'pets'): lambda a, b: f"an owner of {article(b)} {b} lives next to the {a} house",
  ('colors', 'professions'): lambda a, b: f"a {b} lives next to the {a} house",
  ('colors', 'hobbies'): lambda a, b: f"a person who is {b} lives next to the {a} house",
  ('colors', '*'): lambda a, b: f"an owner of {article(b)} {b} lives next to the {a} house",
  ('professions', 'hobbies'): lambda a, b: f"{article(a)} {a}'s neighbour is {b}",
  ('professions', 'pets'): lambda a, b: f"{article(a)} {a}'s neighbour has {article(b)} {b}",
  ('professions', '*'): lambda a, b: f"{article(a)} {a}'s neighbour has {article(b)} {b}",
  ('pets', '*'): lambda a, b: f"{article(a)} {a} lives next to the house with {article(b)} {b}",
  ('hobbies', 'pets'): lambda a, b: f"a neighbour of {article(b)} {b}'s owner is {a}",
  ('hobbies', '*'): lambda a, b: f"a person who is {a} is a neighbour of an owner of {article(b)} {b}",
  ('*', '*'): lambda a, b: f"an owner of {article(a)} {a} is a neighbour of an owner of {article(b)} {b}"
}
  

class SimpleZebraTheme(Theme):
  def repr_OR(self, obj):
    return f"{self.repr(obj.args[0])} or {self.repr(obj.args[1])}"
  
  def repr_AreNeighbours(self, obj):
    cat1, obj1 = obj.args[1]
    cat2, obj2 = obj.args[2]

    if (cat1, cat2) in schema:
      return neighbour_schema[cat1, cat2](obj1, obj2)
    
    if (cat2, cat1) in schema:
      return neighbour_schema[cat2, cat1](obj2, obj1)
    
    if (cat1, '*') in schema:
      return neighbour_schema[cat1, '*'](obj1, obj2)
    
    if (cat2, '*') in schema:
      return neighbour_schema[cat2, '*'](obj2, obj1)


    return schema[('*', '*')](obj1, obj2)

  def repr_SameHouse(self, obj):
    cat1, obj1 = obj.args[1]
    cat2, obj2 = obj.args[2]

    if (cat1, cat2) in schema:
      return schema[cat1, cat2](obj1, obj2)
    
    if (cat2, cat1) in schema:
      return schema[cat2, cat1](obj2, obj1)
    
    if (cat1, '*') in schema:
      return schema[cat1, '*'](obj1, obj2)
    
    if (cat2, '*') in schema:
      return schema[cat2, '*'](obj2, obj1)


    return schema[('*', '*')](obj1, obj2)
  
  def repr_HouseNumber(self, obj):
    cat, x = obj.args[1]
    n = obj.args[2] + 1

    if cat == 'colors':
      return f"the house number {n} is {x}"
    
    if cat in 'professions':
      return f"{article(x)} {x} lives at number {n}"
    
    if cat in 'pets':
      return f"{article(x)} {x} lives in the house number {n}"
    
    if cat in 'hobbies':
      return f"a person who lives at number {n} is {x}"
    
    return f"there is {article(x)} {x} in the house number {n}"