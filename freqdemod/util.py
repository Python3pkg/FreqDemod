#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# util.py
# John A. Marohn
# 2014/06/28

import math

# Modified from http://code.activestate.com/recipes/578238-engineering-notation/

def powerise10(x):
    """ Returns x as a * 10 ^ b with 0<= a <10"""
    if x == 0: return 0 , 0
    Neg = x <0
    if Neg : x = -x
    a = 1.0 * x / 10**(math.floor(math.log10(x)))
    b = int(math.floor(math.log10(x)))
    if Neg : a = -a
    return a ,b

def eng(x):
    """Return a string representing x in an engineer-friendly notation"""
    a , b = powerise10(x)
    if -3<b<3: return "%.4g" % x
    a = a * 10**(b%3)
    b = b - b%3
    return "%.4gE%s" %(a,b)