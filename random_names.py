#!/usr/bin/python3
import argparse
import sys
import os
import random
import textwrap
import re

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

class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def check_opts():
	parser = argparse.ArgumentParser(description="Generate random character names", formatter_class=SmartFormatter)
	parser.add_argument('-d', action='store_true', help="Show debug output (DEFAULT: FALSE)", default=False)
	parser.add_argument('-n', nargs=1, type=int, help='''R|Number of names to generate (DEFAULT: 1)

''', default=1)
	parser.add_argument('-o', type=str, help=textwrap.dedent('''R|\
Name format. (DEFAULT: \'y z\')

z - family name (list)
y - given name (list)
a - gendered given prefix
A - neutral/gendered given prefix
b - gendered given base
B - neutral/gendered given base	
c - gendered given suffix
C - neutral/gendered given suffix
d - gendered family prefix
D - neutral/gendered family prefix
e - gendered family base
E - neutral/gendered family base	
f - gendered family suffix
F - neutral/gendered family suffix
whitespace/delimiters for separator characters like hyphens.

	'''), default="y z")
	parser.add_argument('-em',action='store_false', help="Don't use names gendered as male", default=True)
	parser.add_argument('-ef',action='store_false', help="Don't use names gendered as female", default=True)
	parser.add_argument('-en',action='store_false', help='''R|Don't use names gendered as neutral. Ignored by part categories that include gender neutral names

''', default=True)
	
	parser.add_argument('-dz',action='store_true', help="Allow duplicate names to appear as family names. This only applies to lists. Will throw an error if you do not have enough unique names.", default=False)
	parser.add_argument('-dy',action='store_true', help='''R|Allow duplicate names to appear as given names. This only applies to lists. Will throw an error if you do not have enough unique names.

''', default=False)
	
	parser.add_argument('-pz',action='store_true', help="Print all family list names which fit current gender options", default=False)
	parser.add_argument('-py',action='store_true', help='''R|Print all family list names which fit current gender options

''', default=False)
	parser.add_argument('-pa',action='store_true', help="Print all given prefixes which fit current gender options", default=False)
	parser.add_argument('-pA',action='store_true', help="Print all given prefixes which fit current gender options or gender neutral options", default=False)
	parser.add_argument('-pb',action='store_true', help="Print all given bases which fit current gender options", default=False)
	parser.add_argument('-pB',action='store_true', help="Print all given bases which fit current gender options or gender neutral options", default=False)
	parser.add_argument('-pc',action='store_true', help="Print all given suffixes which fit current gender options", default=False)
	parser.add_argument('-pC',action='store_true', help="Print all given suffixes which fit current gender options or gender neutral options", default=False)
	parser.add_argument('-pd',action='store_true', help="Print all family prefixes which fit current gender options", default=False)
	parser.add_argument('-pD',action='store_true', help="Print all family prefixes which fit current gender options or gender neutral options", default=False)
	parser.add_argument('-pe',action='store_true', help="Print all family bases which fit current gender options", default=False)
	parser.add_argument('-pE',action='store_true', help="Print all family bases which fit current gender options or gender neutral options", default=False)
	parser.add_argument('-pf',action='store_true', help="Print all family suffixes which fit current gender options", default=False)
	parser.add_argument('-pF',action='store_true', help="Print all family suffixes which fit current gender options or gender neutral options", default=False)


	global args
	args=parser.parse_args()
	
	global listOpts
	global buildOpts
	global listDict
	global buildDict
	listOpts = {"z","y"}
	listDict={"z":"family","y":"given"}
	buildOpts = {"a":["p","y","n"],"A":["p","y","y"],"b":["b","y","n"],"B":["b","y","y"],"c":["s","y","n"],"C":["s","y","y"],"d":["p","z","n"],"D":["p","z","y"],"e":["b","z","n"],"E":["b","z","y"],"f":["s","z","n"],"F":["s","z","y"]}
	buildDict = {"p":"prefix","s":"suffix","b":"base","z":"family","y":"given","m":"masculine","f":"feminine","n":"gender neutral"}

def loadfile(desc,filename):
	if not os.path.exists(filename):
		print(desc+" file "+filename+" does not exist")
		quit(1);
	else:
		with open(filename) as file:
			lines=[line.rstrip() for line in file]
		file.close()
		return lines

def dump(which):
	items=[]
	kind=0
	if(which in listOpts):
		items=list(which,0,True)
		kind=1
	elif(which in buildOpts):
		items=build(which,0,True)
		kind=2
	if(len(items)==0 or kind==0):
		print("ERROR 100: NOTHING FOUND WHICH MATCHES PARAMETERS")
		exit()
	out=["FOUND "+str(len(items))+" ITEMS"]
	lw=len(out[0])
	out.append("CRITERIA")
	if(not args.em): out.append("NOT MASCULINE")
	if(not args.ef): out.append("NOT FEMININE")
	if(not args.en): out.append("NOT GENDER NEUTRAL")
	if(kind==1): out.append(listDict[which].upper()+" NAME")
	if(kind==2): 
		if(buildOpts[which][2]=="n"): out.append("NOT GENDER NEUTRAL")
		out.append(buildDict[buildOpts[which][0]].upper())
		out.append(buildDict[buildOpts[which][1]].upper())
	for o in out:
		if(len(o)>lw):lw=len(o)+1
	for o in out:
		print("!!! "+o.center(lw)+" !!!")
	for item in items:
		print(item)
	exit()

def list(which,pos,dump):
	sizef=n
	nnames=loadfile(which.capitalize()+" name list","list.txt")
	
	# Set whether duplicates are allowed to the proper list
	if(which == "z"):
		allowDupes=args.dz
	elif(which == "y"):
		allowDupes=args.dy

	goodnlist=[]
	for name in nnames:
		if(name == ""):
			continue
		kind=str.lower(name[-3])
		gen=str.lower(name[-1])
		if(kind==which or kind=="x"):
			if(toBool[args.en] and gen=='n') or (toBool[args.em] and gen=='m') or (toBool[args.ef] and gen=='f'):
				if(dump):
					goodnlist.append(name)
				else:
					subn=name[:-4]
					goodnlist.append(subn)
	if(not dump):
		random.shuffle(goodnlist)
		if(not allowDupes):
			if(len(goodnlist)<sizef):
				print("ERROR: Not enough unique "+listDict[which]+" names")
				exit()
			while(sizef>0):
				namepool[pos].append(goodnlist.pop())
				sizef -= 1
		else:
			while(sizef>0):
				namepool[pos].append(random.choice(goodnlist))
				sizef -= 1
	else:
		return goodnlist
		

def build(which,pos,dump):
	sizef=n*10
	parts=loadfile(which.capitalize()+" name list","build.txt")

	# BUILD LIST OF ACCEPTABLE GENDERED COMPONENTS
	acceptGen=[]
	if(args.em): acceptGen.append("m")
	if(args.ef): acceptGen.append("f")
	if(buildOpts[which][2]=="y"): acceptGen.append("n")
	if(len(acceptGen)==0):
		print("ERROR 110: Gender options specified do not allow any results")
		exit()
		
	# CHECK IF PART IS CORRECT KIND (FAMILY/GIVEN)
	goodnlist=[]
	parts2=[]
	while(len(parts) > 0):
		part=parts.pop()
		if(part == ""):
			continue
		kind=str.lower(part[-5]) 		# Kind:  Z = Family, Y = Given
		if(buildOpts[which][1]==kind) or (kind == "x"):
			parts2.append(part)
	if(len(parts2) == 0):
		print("ERROR 110: No "+buildDict[buildOpts[which][1]]+" options exist in build.txt")
		exit()
	parts=parts2
	parts2=[]
	while(len(parts) > 0):
		part=parts.pop()
		if(part == ""):
			continue
		place=str.lower(part[-3])		# Place: P = Prefix, B = Base, S = Suffix
		if(buildOpts[which][0]==place):
			parts2.append(part)
	if(len(parts2) == 0):
		print("ERROR 111: No "+buildDict[buildOpts[which][1]]+" "+buildDict[buildOpts[which][0]]+" options exist in build.txt")
		exit()
	parts=parts2
	parts2=[]
	while(len(parts) > 0):
		part=parts.pop()
		if(part == ""):
			continue
		gen=str.lower(part[-1])			# Gen:   M = Masculine, F = Feminine, N = Neutral
		if(gen in acceptGen):
			parts2.append(part)
	if(len(parts2) == 0):
		genError=""
		for g in acceptGen:
			if(genError == ""):
				genError = buildDict[g]
			else:
				genError = genError + " or " + buildDict[g]
		print("ERROR 112: No "+buildDict[buildOpts[which][1]]+" "+buildDict[buildOpts[which][0]]+" "+genError+" options exist in build.txt")
		exit()
	parts=parts2
	for part in parts:
		if(dump):
			goodnlist.append(part)
		else:
			subp=part[:-6] 					# Part:  Part to use
			goodnlist.append(subp)

	if(len(goodnlist)==0):
		print("ERROR No "+""+" options exist in build.txt")
		exit()
	if(not dump):
		while(sizef>0):
			namepool[pos].append(random.choice(goodnlist))
			sizef -= 1
	else:
		return goodnlist

if __name__ == "__main__":
	check_opts()

	# HOW MANY NAMES?

	global n
	if(isinstance(args.n,int)):
		n=args.n
	else:
		n=args.n[0]
	
	# CHECK FOR DUMP VARS
	if(args.pz): dump("z")
	elif(args.py): dump("y")
	elif(args.pa): dump("a")
	elif(args.pA): dump("A")
	elif(args.pb): dump("b")
	elif(args.pB): dump("B")
	elif(args.pc): dump("c")
	elif(args.pC): dump("C")
	elif(args.pd): dump("d")
	elif(args.pD): dump("D")
	elif(args.pe): dump("e")
	elif(args.pE): dump("E")
	elif(args.pf): dump("f")
	elif(args.pF): dump("F")

	# CREATE NAME TEMPLATE
	
	while(len(namepool)<len(args.o)):
		namepool.append([])
	
	# NAME POOL GENERATOR
	
	for NG in enumerate(args.o):
		if(NG[1] in listOpts):
			list(NG[1],NG[0],False)
		elif(NG[1] in buildOpts):
			build(NG[1],NG[0],False)
		else:
			OC=0
			runs=n
			while(OC<runs):
				namepool[NG[0]].append(NG[1])
				OC += 1

	# PIECE TOGETHER NAMES
	if(args.d):
		print("---DEBUG---")
		for DEBUG in namepool:
			print(DEBUG)
		print("---DEBUG---")

	Z=n
	while(Z>0):
		outname=""
		for npart in namepool:
			random.shuffle(npart)
			outname += npart.pop()
		print(outname)
		Z -= 1
