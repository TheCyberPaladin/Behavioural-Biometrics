# -*- coding: utf-8 -*-
"""
* @file KeystrokeDynamics.py
* @brief Keystroke generator capture for L. Antichi Thesis
*
* @author Leonardo Antichi (<leo.antichi@sutd.uniroma3.it>)
* @version 1.7
* @since 1.0
*
* @copyright Copyright (c) 2017-2018 Roma Tre, Italy
* @copyright Apache License, Version 2.0
"""

import win32api
import win32con
import sys
import time
import pickle

def Terminal_Clear(): 
    for i in xrange(30): print "\n"

def Error_Counter(a,b,B,I,S):
	V = {}
	V[0,0] = 0
	for i in xrange(1,len(b)+1): V[0,i] = i
	for i in xrange(1,len(a)+1): V[i,0] = i
	for i in xrange(1,len(a)+1):
		for j in xrange(1,len(b)+1):
			V[i,j] = min(V[i-1,j]+B(a,i-1),V[i,j-1]+I(b,j-1),V[i-1,j-1]+S(a,i-1,b,j-1))
	return V[len(a),len(b)]

def KeystrokeDetector():
    Terminal_Clear()
    print u"La password assegnata: '.tie5Roanl'."
    replace = {190:46,188:44,189:45,192:241}
    MAIUSC,INPUT_PWD,TIME_DATA,INPUT_LENGHT,TIME_PASS,TIME_NOW,p       = 0,[],[],0,0,0,0
    HARD_PWD = u".tie5Roanl"
    INPUT_STORE = ""
    HARD_LENGHT = len(HARD_PWD)
    while True and INPUT_LENGHT!=HARD_LENGHT:
	for i in xrange(256):
	    k = win32api.GetAsyncKeyState(i)
	    if k==-32767:
		if i==16 or i==160: MAIUSC=1
		elif i>=65 and i<=90:
		    if MAIUSC==1: INPUT_PWD.append(unichr(i))
		    else:    INPUT_PWD.append(unichr(i+32))
		    TIME_NOW = time.clock()
		    TIME_DATA.append(TIME_NOW-TIME_PASS)
		    MAIUSC,INPUT_LENGHT,TIME_PASS = 0,INPUT_LENGHT+1,TIME_NOW
		else: 
		    if i==8 and len(INPUT_PWD)>0 and len(TIME_DATA)>0: INPUT_PWD = INPUT_PWD[:-1] ; INPUT_LENGHT = max(INPUT_LENGHT-1,0) ; TIME_DATA = TIME_DATA[:-1]
		    else: 
			if i!=1 and i!=13:
				INPUT_PWD.append(unichr(i) if i not in replace else unichr(replace[i]))
			TIME_NOW = time.clock()
			TIME_DATA.append(TIME_NOW-TIME_PASS)
			INPUT_LENGHT,TIME_PASS = INPUT_LENGHT+1,TIME_NOW
		Terminal_Clear()
		print HARD_PWD
		sys.stdout.write("".join(INPUT_PWD))
		sys.stdout.flush()
    INPUT_STORE = "".join(INPUT_PWD)
    nErrors = Error_Counter(HARD_PWD,INPUT_STORE,lambda x,i:1,lambda x,i:1,lambda x,i,y,j: 0 if x[i]==y[j] else 1)
    print "Number of Errors Detected:"
    print nErrors
    v = TIME_DATA+[nErrors]
    return v
    
if __name__ == "__main__":
    print "\nThis is a Demo for Password authentication with Keystroke Dynamics\n"
    print "@author Leonardo Antichi (<leo.antichi@sutd.uniroma3.it>)"
    print "\nCopyright (c) 2017-2018 Roma Tre, Italy"
    time.sleep(5)

    if len(sys.argv)>1:
    	sys.argv[1] = "./Data/" + sys.argv[1]
	v = KeystrokeDetector()
	with open(sys.argv[1],"wb") as fd: pickle.dump(v,fd)
    else: print "Specifica il nome e l'istanza per il salvataggio nel seguente formato 'NOME_ISTANZA'"
