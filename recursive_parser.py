def recursive_parse(code:str)->any:
    """
    Same as parse(), just using Python's stack to make our lives easier.
    """
    sys.setrecursionlimit(3_333) # Some high number to prevent arrowey from crashing too easily with recursion errors
