def my_map(func, list_):
  return [func(x) for x in list_]

my_map2 = my_map

def my_reduce(func, acc, list_):
  for x in list_:
    acc = func(acc, x)
  return acc
