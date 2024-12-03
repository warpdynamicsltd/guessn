from guessn.themes.theme import Theme

schema = {
  ('colors', 'pets'): lambda a, b: f"{b} lives in a {a} house.",
  ('colors', 'professions'): lambda a, b: f"{b} lives in a {a} house.",
  ('colors', 'hobbies'): lambda a, b: f"An person who lives is a {a} house is {b}.",
  ('colors', '*'): lambda a, b: f"There is a {b} in a {a} house.",
  ('professions', 'hobbies'): lambda a, b: f"{a} is {b}.",
  ('professions', 'pets'): lambda a, b: f"{a} has a {b}.",
  ('professions', '*'): lambda a, b: f"{a} has a {b}.",
  ('pets', '*'): lambda a, b: f"{a} lives in a house with a {b}.",
  ('hobbies', '*'): lambda a, b: f"owner of a {b} is {a}.",
  ('*', '*'): lambda a, b: f"owner of a {a} has {b}."
}
  

class SimpleZebraTheme(Theme):
  def repr_SameHouse(self, obj):
    cat1, obj1 = obj.args[1]
    cat2, obj2 = obj.args[2]

    if (cat1, cat2) in schema:
      return schema[cat1, cat2](obj1, obj2).capitalize()
    
    if (cat2, cat1) in schema:
      return schema[cat2, cat1](obj2, obj1).capitalize()
    
    if (cat1, '*') in schema:
      return schema[cat1, '*'](obj1, obj2).capitalize()
    
    if (cat2, '*') in schema:
      return schema[cat2, '*'](obj2, obj1).capitalize()


    return schema[('*', '*')](obj1, obj2).capitalize()
  
  def repr_HouseNumber(self, obj):
    cat, x = obj.args[1]
    n = obj.args[2] + 1

    if cat == 'colors':
      return f"The house number {n} is {x}."
    
    if cat in 'professions':
      return f"{x} lives at number {n}.".capitalize()
    
    if cat in 'pets':
      return f"{x} lives in the house number {n}.".capitalize()
    
    if cat in 'hobbies':
      return f"A person who lives at number {n} is {x}."
    
    return f"There is a {x} in the house number {n}."