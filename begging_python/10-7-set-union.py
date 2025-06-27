from functools import reduce

my_sets = []
for i in range(10):
    my_sets.append(set(range(i, i+5)))

print(my_sets)
my_set = reduce(set.union, my_sets)
print(my_set)