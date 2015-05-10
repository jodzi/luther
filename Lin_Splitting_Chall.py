# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 18:17:47 2015

@author: josephdziados
"""

import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt

#==============================================================================
# '''Challenge 1'''
# # Read data into pandas dataframe
# df = pd.read_csv('2013_movies.csv')
# 
# # Create intercept only model
# intercept_model = smf.ols("DomesticTotalGross ~ 1", df).fit()
# 
# # When using an intercept only model, what we end up predicting is the mean of our response variable which in this case is the mean of Domestic Total Gross.
# 
# # Plot predictions against actual.
# plt.plot(intercept_model.predict(), df.DomesticTotalGross)
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.title('Predicted vs. Actual - Intercept Only Model')
# 
# #Plot historgram of residuals
# plt.hist(intercept_model.resid)
# 
# # The residuals are not distributed normally.  There are far more residuals closer to the mean and it drops as the higher residuals come into play.  
#==============================================================================

#==============================================================================
# '''Challenge 2'''
# 
# df_clean = df.dropna()
# 
# # Adding Budget to model
# model_1 = smf.ols("DomesticTotalGross ~ Budget", df_clean).fit()
# 
# # Plots budget against gross and plots the line of best fit (predictions).
# plt.figure()
# plt.scatter(df_clean.Budget, df_clean.DomesticTotalGross, label='Observed')
# best_fit = model_1.params['Intercept'] + model_1.params['Budget'] * df_clean.Budget
# plt.plot(df_clean.Budget, best_fit, 'r', label='Fit')
# plt.xlabel('Budget')
# plt.ylabel('Domestic Total Gross')
# plt.title('Budget vs. Domestic Total Gross')
# plt.legend(loc='best')
# plt.xlim(0.0)
# 
# plt.figure()
# plt.scatter(df_clean.Budget, model_1.resid, label='Residuals')
# plt.xlabel('Budget')
# plt.ylabel('Residuals')
# plt.title('Residuals vs. Budget')
# plt.legend(loc='best')
# 
# # It appears that there is a cone shape to the residuals of this model.  There is much more variation in the residuals as budget gets larger whereas it should be more normally distributed around 0.  In other words, the higher the budget gets, the less accurate our predictions are.  
#==============================================================================

#==============================================================================
# '''Challenge 3 & 4'''
# 
# # Pulling in my data
# my_df = pd.read_csv('dataframe.csv')
# my_df_clean = my_df.dropna()
# my_df_clean.head()
# 
# # Run the model on transformed variables like log of UK Gross and log of the budget as well as the british factor multiplied by the genre.
# my_model = smf.ols("np.log(UK_Total_Gross) ~ np.log(Budget) + British * Genre", my_df_clean).fit()
# 
# # When adding genre to the model, it appears to increase my R-squared by quite a bit.  This is worrisome to me because it doesn't make sense and it will have to be looked into further.  The genre's all have a "base" genre which is action and the rest of the genres are being compared on performance to that base.  
#==============================================================================

#==============================================================================
# '''Challenge 5'''
# df_train = my_df_clean[:750]
# df_test = my_df_clean[750:]
# 
# model_train = smf.ols("np.log(UK_Total_Gross) ~ np.log(Budget) + British * Genre", df_train).fit()
# 
# Y_pred = model_train.predict(df_test)
# 
# plt.scatter(Y_pred, np.log(df_test.UK_Total_Gross))
# plt.xlabel('Prediction')
# plt.ylabel('Actual')
# plt.title('Predictions vs. Actual')
#==============================================================================
