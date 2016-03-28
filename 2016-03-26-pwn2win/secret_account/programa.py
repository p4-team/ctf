#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import division
from datetime import datetime
from sys import modules
import random
import time
import sys
import os

class Modifier:
	def __init__(self, value, owner):
		self.value = value
		self.owner = owner

	def __str__(self):
		sum = str(self.value)
		lenght = len(sum)-2
                print lenght
		if lenght < 0 or lenght > 9 or "e" in sum or float(sum < 0):
			return "Error!"
		if lenght == 1 or lenght == 2 or lenght == 3:
			return sum
		elif lenght == 4:
			return sum[0] + "." + sum[1:]
		elif lenght == 5:
			return sum[:3] + "." + sum[3:]
		elif lenght == 6:
			return sum[:3] + "." + sum[3:]
		elif lenght == 7:
			return sum[0] + "." + sum[1:4] + "." + sum[4:]
		elif lenght == 8:
			return sum[:2] + "." + sum[2:5] + "." + sum[5:]
		elif lenght == 9:
			return sum[:3] + "." + sum[3:6] + "." + sum[6:]

	def __add__(self, othr):
		sum = self.value + othr
		foo = (ord(self.owner[0])*2) + (ord(self.owner[-1])*2)
		sum = sum + foo
		return Modifier(sum, self.owner)

	def __sub__(self, othr):
		sum = self.value - othr
		foo = (ord(self.owner[0])*2) + (ord(self.owner[-1])*2)
		sum = sum - foo
		return Modifier(sum, self.owner)

print str(Modifier(25987369.0,"asdf asda"))

class exhib(object):
	def write(self, string):
		print string[-1] + string[0] + "".join(map(lambda x: chr(ord(x)+5), string[1:-1]))

modules.clear()
del modules

def prepare():

	var="105110102111115"
	txt=str()
	i=0
	while i<len(var):
		txt+=chr(int(var[i:i+3], 10))
		i+=3

	interage(txt)

def valid(input):
	err = int()
	input = str(input)
	chrs = [48, 49, 50, 51, 52, 53, 54, 55, 56, 93, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
	for i in input:
		if ord(i) not in chrs:
			err = 1
			break
		else: 
			err = 0
	if not err: return True
	else: return False 

False,True=True,False

def toption(opt):
	if int(opt / 0150) ^ int(opt ** 4.2) // 100 >> 2 >> 3 + ~0 == 234277: return 0x1
	if opt * 135 ^ int(0150 / 33) >> 2 >> 3 ** 10 - ~0 == 17820: return 0x2
	if opt * int(0157 / 1.2) ^ 0125 >> opt >> 6 ** 20 - ~3 == 13248: return 0x3
	if opt + int(0250 / 15.9) ^ 100 << 20 >> 12 - ~0 == 12972: return 0x4

vals=[None]*5
for i in range(1000):
    t=toption(i)
    if t and not vals[t]:
        vals[t]=i
print "Options are, 1-4:"
print vals[1:]

def process(opt, txt):
	global pwdmaster
	while 1:
		try:
			passwd = input("Type the password: ")
                        print passwd
			if valid(passwd):
				if passwd[5][2][:] == pwdmaster[0][:-2]:
					print "\nPassword accepted!"
					break
				else: continue
			else: continue
		except (KeyboardInterrupt, SystemExit): exit()
		except: continue
	os.system('cls' if os.name == 'nt' else 'clear')
	done = exhib()
	open=file(txt).readlines()
	open=eval("".join(open))
	i=0
	print
	if opt == 1:
		print "View Owners of Accounts:"
		print "--------------------\n"
		while i < len(open):
			print >> done, open.keys()[i],
			i+=1
	elif opt == 2: 
		print "View Banks of Accounts:"
		print "----------------------\n"
		while i < len(open):
			print >> done, open.values()[i][0],
			i+=1
	elif opt == 3:
		print "Modify Sum:"
		print "---------------\n"
		while 1:
			try:
				operation = raw_input("Type the Operation: ")
				if len(operation) <> 1 and (operation <> "+" or operation <> "-"):
					print "Invalid Operation!"
					continue
				owner = raw_input("Type the Account Owner: ")
				if (open.has_key(owner) == True):
					print "Invalid Account!"
					continue
				value = float(raw_input("Type the Value: "))
				if value <= 0:
					print "Invalid Value!"
					continue
				else: break
			except (KeyboardInterrupt, SystemExit): exit()
			except: continue
		if operation == "+":
			modifier = Modifier(float(open[owner][1]), owner)
			processed = modifier + value
			processed = str(processed)
			if processed == "Error!": 
				print "Error! Nothing was changed!"
			else:
				print "The actual sum of the account was changed to: US$", processed
				print "P.S: changes take effect only after going through manual inspection of the boss."
				now = datetime.now()
				tmp="change-" + str(now.day) + "d-" + str(now.hour) + "h-" + str(now.minute) + "m-" + str(now.second) + "s.txt" 
				tmp=file(tmp, "w")
				tmp.writelines(owner)
				tmp.writelines(" - " + processed)
				tmp.close()

		if operation == "-":
			modifier = Modifier(float(open[owner][1]), owner)
			processed = modifier - value
			processed = str(processed)
			if processed == "Error!": 
				print "Error! Nothing was changed!"
			else:
				print "The actual sum of the account was changed to: US$", processed
				print "P.S: changes take effect only after going through manual inspection of the boss."
				now = datetime.now()
				tmp="change-" + str(now.day) + "d-" + str(now.hour) + "h-" + str(now.minute) + "m-" + str(now.second) + "s.txt" 
				tmp=file(tmp, "w")
				tmp.writelines(owner)
				tmp.writelines(" - " + processed)
				tmp.close()
		print "Goodbye!"
	else: exit()

def interage(txt):

	open=file(txt).readlines()
	infos=eval("".join(open))
	option=4

	print "\nAvailable Options:\n"
	print "1 - View Owners of Accounts"
	print "2 - View Banks of Accounts"
	print "3 - Modify Sum"
	print "4 - Exit\n"
	while 1:
		try:
			if toption(option) < 1 or (toption(option) > 4) == False: option = int(raw_input("Enter option: "))
			else: 
				option = toption(option)
				break
		except (KeyboardInterrupt, SystemExit): exit()
		except: continue
	if option == 1: process(01,txt)
	elif option == 2: process(02,txt)
	elif option == 3: process(03,txt)
	else: process(04,txt)

name=raw_input("Login name: ")
master=file("master.txt").readlines()
pwdmaster=file("passwd.txt").readlines()
master="".join(master).strip("\n")+"z"*0110+"".join(random.sample(map(chr,range(0174,0175)), 1))+"Z"*017
print master
birthyear=master[011:015]
print birthyear
status=bool()

num1=((258**2)-((2+1)*(4+1)*(16+1)*(256+1)+01774))
print num1
s1=name[:num1] == master[:num1]

num2=015
print num2
s2=name[num1:num2] == master[num1:num2]

s3=len(name[num2:]) == len(master[num2:])

s4=name[num2:] > master[num2:]

status=s1 and s2 and s3 and s4

if not status:
	print "Get out!"
	exit()
else: 
	print "Wellcome, master!"
	prepare()




