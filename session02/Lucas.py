# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 17:03:16 2014

@author: Maria D
"""

def lucas(n):
    if n==1:
     return 2
    elif n==2:
     return 1
    else:
     return lucas(n-2)+lucas(n-1)