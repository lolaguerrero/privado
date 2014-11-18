def fib(n):
    """Return the nth  value in the fibonacci function, which is a recursive function. """
    if n == 0:
        return 0
    elif n == 1:   
        return 1           
    else:                      
        return fib(n-1) + fib(n-2)

# print fib(7)


def lucas(n):
    """Return the nth value in the Lucas function, which is also a recursive function but starts with 2 and 1 rather than 0 and 1"""
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return lucas(n-1) + lucas(n-2)
# print lucas (2)
# print lucas (7)


def sum_series(n, x=0,y=1):
    """ Return the nth value of a recursive function. There are two optional parameters, x and y.
        x is the first 0th value and y is the 1st value.

        When x = 0 and y = 1, the result is the fibbonacci sequence
        When x = 2 and y = 1, the result is the lucas sequence
        When x  and y are other values, there are different sequences
    """
    if n == 0:
        return x
    elif n == 1:
        return y
    else:
        return sum_series(n-1, x, y) + sum_series(n-2, x, y) # it took me a while to figure out why it was going back to fibbonacci 
                                                                                        # even when x =2, of course have to re-add x and y in the else part!!!
# print sum_series(0,2)
# print sum_series(1,0,4)
# print sum_series(2)
# print sum_series(7)
# print sum_series(7,2)
# print sum_series(7,3,1)


if __name__ == "__main__":
    assert fib(7) == 13
    assert lucas (7) == 29
    assert sum_series(7) == 13
    assert sum_series(7,2) == 29
    assert sum_series(7,3) == 37

print "all good here"