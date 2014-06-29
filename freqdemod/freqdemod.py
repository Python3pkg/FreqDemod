#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# freqdemod.py
# John A. Marohn
# 2014/06/28

"""

Summary
-------

Overview
--------

We demodulate the signal in the following steps:

1. Apply a window to the signal :math:`S(t)` in order to make it smoothly ramp up from zero and ramp down to zero.

2. Fast Fourier Transform the windowed signal to obtain :math:`\\hat{S}(f)`.

3. Identify the primary oscillation frequency :math:`f_0`.  Apply a bandpass filter centered at :math:`f_0` to reject signals at other frequencies.

4. Apply a second filter which zeros out the negative-frequency components of :math:`\\hat{S}(f)`.

5. Apply an Inverse Fast Fourier Transform to the resulting data to obtain a complex signal :math:`z(t) = x(t) + i \: y(t)`.

6. Compute the instantaneous phase :math:`\\phi` and amplitude :math:`a(t)` using the following equations. Unwrap the phase.

.. math::
    :label: Eq;phi
        
    \\begin{equation}
    \\phi(t) = \\arctan{[\\frac{y(t)}{x(t)}]}
    \\end{equation}

.. math::
    :label: Eq:a

    \\begin{equation}
    a(t) = \\sqrt{x(t)^2 + y(t)^2}
    \\end{equation}

7. Calculate the "instantaneous" frequency :math:`f(t)` by dividing the instantaneous phase data into equal-time segments and fitting each segment to a line.  The average frequency :math:`f(t)` during each time segment is the slope of the respective line.


"""

import numpy as np
import math
import copy
from util import eng


class Signal(object):

    def __init__(self, s, s_name, s_unit, dt):
        
        """Initialze the Signal object, with
        
            :s: the signal *vs* time, a ``numpy`` array 
            :s_name: the signal's name, a string
            :s_name: the signal's units, a string
            :dt: the time per point [s], a floating-point number
            
        We cast the input ``s`` into a ``numpy`` array just in case the user passes the function a list instead.            
            
        """    

        signal = {}

        signal['s'] = np.array(s)
        signal['s_name'] = s_name
        signal['s_unit'] = s_unit
        signal['dt'] = dt
        
        signal['s_original'] = np.array([])        
        
        self.signal = signal
        
    def binarate(self,mode):

        """Truncate the signal, if needed, so it is a factor of two in length.  
        How this is done depends on the ``mode``, which may be "start","middle",
        or "end".  The function redefines the signal `s` and saves a copy of the
        original signal in `s_original`.
        
        """

        self.signal['s_original'] = copy.deepcopy(self.signal['s'])

        n = len(self.signal['s'])
        n2 = int(math.pow(2,int(math.floor(math.log(n, 2)))))
        
        if mode == "middle":
                  
            n_start = int(math.floor((n - n2)/2))
            n_stop = int(n_start + n2)
            array_indices = list(np.arange(n_start,n_stop)) 

        elif mode == "start": 
            
            array_indices = list(np.arange(0,n2))
            
        elif mode == "end":
            
            array_indices = list(np.arange(n-n2,n))
            
        self.signal['s'] = self.signal['s'][array_indices]
                
        
    def __repr__(self):
        """ Make a report of the (original) signal's properties including its 
        name, unit, time step, rms, max, and min.
        """
        
        s_rms = np.sqrt(np.mean(self.signal['s']**2))
        s_min = np.min(self.signal['s'])
        s_max = np.max(self.signal['s'])
        
        temp = []
        temp.append("Signal")
        temp.append("======")
        temp.append("signal name: {0}".format(self.signal['s_name']))
        temp.append("signal unit: {0}".format(self.signal['s_unit']))
        temp.append("signal lenth = {}".format(len(self.signal['s'])))
        temp.append("time step = {0:.3f} us".format(self.signal['dt']*1E6))
        temp.append("rms = {}".format(eng(s_rms)))
        temp.append("max = {}".format(eng(s_max)))
        temp.append("min = {}".format(eng(s_min)))
        
        return '\n'.join(temp)
        
    