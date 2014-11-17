# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 16:31:22 2014

@author: Maria D
"""

def fibo(n):
    if n==0:
     return 0
    elif n==1:
     return 1
    else:
     return fibo(n-2)+fibo(n-1)