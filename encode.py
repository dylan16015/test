#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 23:13:35 2019

@author: dylan
"""
import re

alphabet = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i', 9:'j', 10:'k', 11:'l', 12:'m', 13:'n', 14:'o', 15:'p', 16:'q'
       , 17:'r', 18:'s', 19:'t', 20:'u', 21:'v', 22:'w', 23:'x', 24:'y', 25:'z'}

#ROTOR CONFIGURATION
rotor_0 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
rotor_1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
rotor_2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
rotor_3 = [17, 2, 3, 4, 0, 18, 19, 20, 21, 22, 23, 24, 25, 5, 6, 7, 8, 1, 16, 15, 14, 13, 12, 11, 10, 9]
rotor_4 = [3, 11, 17, 21, 19, 20, 24, 25, 23, 22, 18, 14, 13, 15, 16, 12, 6, 2, 7, 10, 8, 1, 9, 5, 4, 0]
rotor_5 = [2, 7, 10, 8, 1, 9, 5, 4, 0, 3, 11, 17, 21, 19, 20, 24, 25, 23, 22, 18, 14, 13, 15, 16, 12, 6]
reflector = [13,12,11,10,9,8,25,24,23,22,21,20,19,18,4,3,2,1,0,17,16,15,14,7,6,5] 

#USER INPUT
plug_settings = [[6,23], [22,3], [14,24], [0,16], [15,1], [2,11], [5,13], [21,17], [16, 20], [10, 19]]

rotors = [rotor_3, rotor_4, rotor_5]

rotor_setting = [5,2,13]

text = 'encryption'

rotor_kick_point = [6, 3]

def clean(text):
    text = str(text).lower()
    text = re.sub("[^a-z]+", "", text)
    return text

def rotor_wiring_offset(r):
    nr = []
    for i in range(len(r)):
        nr.append(r[i] - i)
    return nr

def rotor_setting_offset(r, s):
    nr = list(r)
    for i in range(len(r)):
        if s<0:
            r[i+s] = nr[i]
        else:
            r[i] = nr[i-s]
    return r

def reverse_rotor_flow(l):    
    r = rotor_wiring_offset(l)
    d = {}
    for i in range(len(r)):
        d[l[i]] = -r[i]
    d = dict(sorted(d.items()))
    d = list(d.values())
    return d

def rotate(n):
    if n >= 26:
        n -= 26
    elif n < 0:
        n += 26
    return n

def ring_setting(l):
    pass

def test(x):
    print('test'*x)
    
def encode(alphabet, plug_settings, rotors, rotor_setting, rotor_kick_point, text):
    numbers = dict((v,k) for k,v in alphabet.items())
    
    ref = rotor_wiring_offset(reflector)
    
    output = []
    
    plugs = {}
#    for i in range(len(plug_settings)):
#        plugs[plug_settings[i][0]] = plug_settings[i][1]
#        plugs[plug_settings[i][1]] = plug_settings[i][0]
    for i in range(len(plug_settings)):
        a = alphabet[plug_settings[i][0]]
        b = alphabet[plug_settings[i][1]]
        c = alphabet[plug_settings[i][1]]
        d = alphabet[plug_settings[i][0]]
        plugs[a] = c
        plugs[b] = d      
    
    for char in text:
                    
        if rotor_setting[0] == rotor_kick_point[0]:
            rotor_setting[1] += 1
            if rotor_setting[1] == rotor_kick_point[1]:
                rotor_setting[2] += 1
        if rotor_setting[0] == 26:
            rotor_setting[0] -= 26 
        if rotor_setting[1] == 26:
            rotor_setting[1] -= 26
        if rotor_setting[2] == 26:
            rotor_setting[2] -= 26

        r0 = rotor_wiring_offset(rotors[0])
        r1 = rotor_wiring_offset(rotors[1])
        r2 = rotor_wiring_offset(rotors[2])
    
        r0 = rotor_setting_offset(r0, rotor_setting[0])
        r1 = rotor_setting_offset(r1, rotor_setting[1])
        r2 = rotor_setting_offset(r2, rotor_setting[2])

        if char in plugs.keys():
            char = plugs[char]
        
        char = numbers[char]

        pos = r0[char] + char
        char = rotate(pos)
        
        pos = r1[char] + char
        char = rotate(pos)
        
        pos = r2[char] + char
        char = rotate(pos)       
        
        pos = ref[char] + char
        char = pos
        
        r0 = rotor_setting_offset(reverse_rotor_flow(rotors[0]), rotor_setting[0])
        r1 = rotor_setting_offset(reverse_rotor_flow(rotors[1]), rotor_setting[1])
        r2 = rotor_setting_offset(reverse_rotor_flow(rotors[2]), rotor_setting[2])
        
        pos = r2[char] + char
        char = rotate(pos)
        
        pos = r1[char] + char
        char = rotate(pos)
                      
        pos = r0[char] + char
        char = rotate(pos)            
        
        char = alphabet[char]
        
        if char in plugs.keys():
            char = plugs[char]
            
        output.append(char)
        rotor_setting[0] += 1

    return ''.join(output)
    
#mode = input("Would you like to 'encode' or 'decode'?")
#text = input("Please enter text...")   
        
if __name__=='__main__':
    

    print(encode(alphabet, plug_settings, rotors, rotor_setting, rotor_kick_point, text))
