import sys

def reverser(to_reverse):
    if to_reverse == "":
        return to_reverse
    else:
        return to_reverse[-1] + reverser(to_reverse[:-1])

for line in sys.stdin:
    print reverser(line.rstrip())
