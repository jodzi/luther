# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 09:16:01 2015

@author: josephdziados
"""

import numpy as np
import matplotlib.pyplot as plt

test = np.linspace(0.0, 10.0, num = 101)

prob_nums = np.array([2.0,7.0,1.0,5.0,10.0])

sums = []

for num in test:
    sums.append(np.sum((prob_nums - num) ** 2))    
    
#aarons code
#sos = np.vectorize(lambda x, data:  sum((data - x)**2), excluded=[1])
#results = sos(test, prob_nums)
    
index = sums.index(min(sums))
print test[index]

plt.plot(test, sums)
plt.xlabel("Candidate Numbers")
plt.ylabel("Sum Values")
