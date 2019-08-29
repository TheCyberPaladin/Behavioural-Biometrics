#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* @file Authenticator.py
* @brief Keystroke generator capture for L. Antichi Thesis
*
* @author Leonardo Antichi (<leo.antichi@sutd.uniroma3.it>)
* @version 1.7
* @since 1.0
*
* @copyright Copyright (c) 2017-2018 Roma Tre, Italy
* @copyright Apache License, Version 2.0
"""

from sklearn.svm import OneClassSVM
import pickle
import time
from os import listdir
import numpy as np
import KeystrokeDynamics

## Train SVC ##
Database = listdir("./Data")
user_data = []

for t in Database:
    y = t[:t.find("_")]
    with open("./Data/"+t,"rb") as fd: x = pickle.load(fd)
    user_data.append(np.array(x))

clf = OneClassSVM(kernel='rbf', gamma='auto')
clf.fit(user_data)

##################
print "\nThis is a Demo for Password authentication with Keystroke Dynamics\n"
print "@author Leonardo Antichi (<leo.antichi@sutd.uniroma3.it>)"
print "\nCopyright (c) 2017-2018 Roma Tre, Italy"
time.sleep(5)
epsilon = 0.1
v = KeystrokeDynamics.KeystrokeDetector()
KeystrokeDynamics.Terminal_Clear()

res = clf.decision_function([v])

print res
if abs(res)<epsilon:
    print "\nThe user is authenticated!"
else:
    print "\nIntruder detected, please perform again the authentication."



