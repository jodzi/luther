# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:09:51 2015

@author: josephdziados
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
import random
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

#'''Challenge 1'''
#def simulate_outcomes(budget, sigma):
#    return model.params['const'] + model.params['x1'] * budget + random.gauss(0, sigma)
#
#df = pd.read_csv('2013_movies.csv')
#df = df.dropna()
#
#const = np.ones(len(df))
#X = np.column_stack((np.log(df.Budget), const))
#y = np.log(df.DomesticTotalGross)
#
#model = sm.OLS(y,X).fit()
#
#sigma = np.std(model.resid)
#y_predict = [simulate_outcomes(np.log(df.Budget.ix[i]), sigma) for i in df.index]
#
#plt.figure()
#plt.scatter(np.log(df.Budget), y_predict)
#plt.xlabel('log Budget')
#plt.ylabel('log Total Domestic Gross')
#plt.title('Simulated Model Results')
#plt.figure()
#plt.scatter(np.log(df.Budget), np.log(df.DomesticTotalGross))
#plt.xlabel('log Budget')
#plt.ylabel('log Total Domestic Gross')
#plt.title('Actual Observed Data')

'''Challenge 2'''



#'''Challenge 3'''
#df_train = df[:75]
#df_test = df[75:]
#const = np.ones(len(df_train))
#const2 = np.ones(len(df_test))
#
#X_train = np.column_stack((const, np.log(df_train.Budget)))
#y_train = np.log(df_train.DomesticTotalGross)
#regr = LinearRegression()
#regr.fit(X_train, y_train)
#y_pred_train = regr.predict(X_train)
#train_MSE = mean_squared_error(np.log(df_train.DomesticTotalGross), y_pred_train)
#print 'Training MSE: {0:.2f}'.format(train_MSE)
#
#
#X_test = np.column_stack((const2, np.log(df_test.Budget)))
#y_pred_test = regr.predict(X_test)
#test_MSE = mean_squared_error(np.log(df_test.DomesticTotalGross), y_pred_test)
#print 'Test MSE: {0:.2f}'.format(test_MSE)

'''Challenge 4'''
train_mse = []
test_mse = []
r_squared = []

x = np.reshape(np.log(df.Budget),[87,1])
y = np.reshape(np.log(df.DomesticTotalGross), [87,1])

for i in range(0,8):
    regr = LinearRegression()
    if i == 0:
        cons_0 = np.reshape(np.ones(len(df)), [87,1])
        regr.fit(cons_0, y)
        r_squared.append(regr.score(cons_0, y))
        regr.fit(X_train[:,0,np.newaxis], y_train)
        y_pred_0 = regr.predict(X_train[:,0,np.newaxis])
        train_mse.append(mean_squared_error(np.log(df_train.DomesticTotalGross), y_pred_0))
        y_pred_test_0 = regr.predict(X_test[:,0,np.newaxis])
        test_mse.append(mean_squared_error(np.log(df_test.DomesticTotalGross), y_pred_test_0))
    else:
        regr.fit(x**i, y)  
        r_squared.append(regr.score(x**i, y))
        regr.fit(X_train ** i, y_train)
        y_train_pred = regr.predict(X_train ** i)
        train_mse.append(mean_squared_error(np.log(df_train.DomesticTotalGross), y_train_pred))
        y_test_pred = regr.predict(X_test ** i)
        test_mse.append(mean_squared_error(np.log(df_test.DomesticTotalGross), y_test_pred))

plt.subplot(2,2,1)
plt.plot(range(0,8), r_squared)
plt.subplot(2,2,2)
plt.plot(range(0,8), train_mse)
plt.subplot(2,2,3)
plt.plot(range(0,8), test_mse)