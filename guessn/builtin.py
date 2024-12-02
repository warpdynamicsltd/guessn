from guessn.core import Predicate, Term

add = Term(lambda a, b: a + b, '+', f'%s + %s', ['A', 'B'])
sub = Term(lambda a, b: a - b, '-', f'%s - %s', ['A', 'B'])
mul = Term(lambda a, b: a * b, '*', f'%s * %s', ['A', 'B'])
divides = Predicate(lambda a, b: b % a == 0, f'%s | %s', ['A', 'B'])