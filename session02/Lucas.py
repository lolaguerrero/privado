# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 17:03:16 2014

@author: Maria D
"""

def lucas(n):
    """ The Lucas Numbers are a related series 
    of integers that start with the values 2 and 1
    rather than 0 and 1"""
    if n==1:
     return 2
    elif n==2:
     return 1
    else:
     return lucas(n-2)+lucas(n-1)