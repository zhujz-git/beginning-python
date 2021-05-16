import fileinput

for line in fileinput.input():
    print('{:<50} # {:2d}'.format(line.rstrip(), fileinput.lineno()))