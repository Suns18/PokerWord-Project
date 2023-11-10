"""all mothod"""
import random
lstmethod = ['capitalize', 'casefold', 'center', 'count', 'encode', \
             'endswith', 'expandtabs', 'find', 'format', 'format_map', \
             'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', \
             'isdigit', 'isidentifier', 'islower', 'isnumeric', \
             'isprintable', 'isspace', 'istitle', 'isupper', 'join', \
             'ljust', 'lower', 'lstrip', 'maketrans', 'partition', \
             'repalce', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', \
             'rstrip', 'split', 'splitlines', 'strip', 'swapcase', 'title', \
             'upper', 'zfill', 'append', 'clear', 'copy', 'extend', 'insert', \
             'pop', 'remove', 'reverse', 'sort', 'fromkeys', 'get', 'items', \
             'keys', 'popitem', 'setdefault', 'update', 'values', 'add', \
             'difference', 'difference_update', 'discard', 'intersection', \
             'intersection_update', 'isdisjoint', 'issubset', \
             'symmetric_difference', 'symmetric_difference_update', 'union', \
             'close', 'detach', 'fileno', 'flush', 'isatty', 'read', \
             'readable', 'readline', 'readlines', 'seek', 'seekable', 'tell', \
             'truncate', 'writable', 'write', 'writelines', 'seed', 'getstate', \
             'setstate', 'getrandbits', 'randrange', 'randint', 'choice', \
             'shuffle', 'sample', 'random', 'uniform', 'triangular', 'betariate', \
             'expovariate', 'gammavariate', 'gauss', 'lognormvariate', \
             'normalvariate', 'vonmisesvariate', 'paretovariate', 'weibullvariate', \
             'delete', 'head', 'patch', 'post', 'put', 'request']
lstmethodimport = ['harmonic_mean', 'mean', 'median', 'median_grouped', 'median_high', \
                   'median_low', 'mode', 'pstdev', 'stdev', 'pvariance', 'variance', \
                   'acos', 'acosh', 'asin', 'asinh', 'stan', 'atan2', 'atanh', 'ceil', \
                   'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'erf', 'erfc', \
                   'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', \
                   'gamma', 'gcd', 'hypot', 'isclose', 'isfinite', 'isinf', 'isnan', \
                   'isqrt', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'perm', \
                   'pow', 'prod', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', \
                   'tanh', 'trunc', 'phase', 'polar', 'rect', 'loads', 'dumps', \
                   'datetime', 'search', 'sub', 'findall']
score = { "a": 1, "b": 4, "c": 3, "d": 2, "e": 1, "f": 3, "g": 4, "h": 4, "i": 1, \
         "j": 5, "k": 5, "l": 2, "m": 3, "n": 2, "o": 2, "p": 2, "q": 5, "r": 1, \
            "s": 1, "t": 1, "u": 3, "v": 4, "w": 5, "x": 5, "y": 5, "z": 5}
lstans = []
bear_HP = 100
my_HP = 30
shield = 0
skip = False
count = 0
heal_card = 0
shield_card = 0
power_card = 0
freeze_card = 0
my_card = ["heal_card", "shield_card", "power_card", "freeze_card"]
while True:
   attact = 0
   word = input()
   if word in lstmethod or word in lstmethodimport:
      for char in word:
         attact += score[char]
      if count == 0:
         lstans.append(word)
         count += 1
      elif count == 3:
         lstans.clear()
         count = 0
         card_increase = random.choice(my_card)
         if card_increase == "heal_card":
            heal_card += 1
         elif card_increase == "shield_card":
            shield_card += 1
         elif card_increase == "power_card":
            power_card += 1
         elif card_increase == "freeze_card":
            freeze_card += 1
      elif count >= 1 and word in lstans:
         count = 0
   else:
      count = 0
   #ใช้การ์ดพิเศษ
   if heal_card:
      my_HP += 10
      bear_HP -= random.uniform(attact*0.2, attact)
   elif shield_card:
      shield += 2
      bear_HP -= random.uniform(attact*0.2, attact)
   elif power_card:
      bear_HP -= attact
   elif freeze_card:
      bear_HP += 10
      skip = True
   if skip:
      skip = False
   elif shield > 0:
      shield -= 1
   elif bear_HP <= 20:
      my_HP -= 10
   elif bear_HP <= 50:
      my_HP -= 5
   elif bear_HP <= 100:
      my_HP -= 3
   if bear_HP <= 0:
      print("You Win")
      break
   elif my_HP <= 0:
      print("You Lose")
      break