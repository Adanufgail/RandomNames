#!/usr/bin/python3
import argparse
import sys
import os
import random

'''
TODO:
PREFIX/SUFFIX
NOT ONLY 2 NAMES (1,3+)
ABILITY TO GENDER LAST NAMES
ABILITY TO MIX GENDER BASED ON NAME POSITION
ABILITY TO USE FIRST NAMES AS A LAST NAME BASE
'''

toBool = {'True':True,'False':False,True:True,False:False}
namepool=[]

def check_opts():
	parser = argparse.ArgumentParser(description="Generate random character names")
	parser.add_argument('-n', nargs=1, type=int, help="Number of names to generate (DEFAULT: 1)", default="[1]")
	parser.add_argument('-fs',choices=['True','False'], type=str.capitalize, help="Use first name prefixes/suffixes (DEFAULT: FALSE)", default=False)
	parser.add_argument('-ls',choices=['True','False'], type=str.capitalize, help="Use last name prefixes/suffixes (DEFAULT: FALSE)", default=False)
	parser.add_argument('-fl',choices=['True','False'], type=str.capitalize, help="Use first name list (DEFAULT: TRUE)", default=True)
	parser.add_argument('-ll',choices=['True','False'], type=str.capitalize, help="Use last name list (DEFAULT: TRUE)", default=True)
	parser.add_argument('-gm',choices=['True','False'], type=str.capitalize, help="Use names gendered as male (DEFAULT: FALSE)", default=False)
	parser.add_argument('-gf',choices=['True','False'], type=str.capitalize, help="Use names gendered as female (DEFAULT: FALSE)", default=False)
	parser.add_argument('-gn',choices=['True','False'], type=str.capitalize, help="Use names gendered as neutral (DEFAULT: TRUE)", default=True)

	global args
	args=parser.parse_args()

def loadfile(desc,filename):
	if not os.path.exists(filename):
		print(desc+" file "+filename+" does not exist")
		quit(1);
	else:
		with open(filename) as file:
			lines=[line.rstrip() for line in file]
		file.close()
		return lines

def list(which,pos):
	sizef=int(args.n[0])*10
	nnames=loadfile(which.capitalize()+" name list",which+"_list.txt")
	goodnlist=[]
	for name in nnames:
		if(name == ""):
			continue
		subn=name[:-2]
		gen=str.lower(name[-1])
		#print(str(toBool[args.gn])+","+str(toBool[args.gm])+","+str(toBool[args.gf]))
		if(toBool[args.gn] and gen=='n') or (toBool[args.gm] and gen=='m') or (toBool[args.gf] and gen=='f') or (pos == namecount-1):
			goodnlist.append(subn)
	
	while(sizef>0):
		namepool[pos].append(random.choice(goodnlist))
		sizef -= 1

if __name__ == "__main__":
	check_opts()

	# HOW MANY NAMES?
	# HARDCODED FOR NOW?
	
	namecount=2

	while(len(namepool)<namecount):
		namepool.append([])
	
	# FIRST NAME POOL GENERATOR
	
	# USE NAME LIST?
	if(toBool[args.fl]):
		list("first",0)
	if(toBool[args.ll]):
		list("last",1)

	# USE PREFIX/SUFFIX?

	# PIECE TOGETHER NAMES

	Z=args.n[0]
	while(Z>0):
		outname=""
		for npart in namepool:
			random.shuffle(npart)
			if(outname != ""):
				outname += " "
			outname += npart.pop()
		print(outname)
		Z -= 1
