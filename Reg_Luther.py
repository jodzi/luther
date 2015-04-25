# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:17:22 2015

@author: josephdziados
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import numpy as np
import seaborn as sns
sns.set_context('poster')

final_df = pd.read_csv('dataframe.csv')

plt.scatter(final_df['Budget'], final_df['UK_Total_Gross'])

model =  smf.ols("np.log(UK_Total_Gross) ~ np.log(Budget) + Genre * British", final_df).fit()

#print model.summary()

#==============================================================================
# #Permutation test to check my British coefficient
# british_coef = []
# 
# 
# for i in range(1000):
#     subset = final_df.take(np.random.permutation(len(final_df))[:400])
#     model = smf.ols("np.log(UK_Total_Gross) ~ np.log(Budget) + Genre * British", subset).fit()
#     british_coef.append(model.params['British'])
#==============================================================================

#==============================================================================
# sns.set_palette("pastel")
# plt.rc("figure", figsize=(8, 4))
# british_label = "Average Difference (mean: " + str(round(np.mean(british_coef), 2)) + ")"
# sns.distplot(british_coef, label=british_label);
# plt.legend(loc='best')
# plt.xlabel('British Factor')
# plt.ylabel('Count')
# plt.title('Simulation of British Factor')
#==============================================================================

    


