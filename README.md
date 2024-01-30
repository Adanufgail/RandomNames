# RandomNames
Generate random character names for TTRPG.

# Usage

'''
usage: random_names.py [-h] [-d] [-n N] [-o O] [-em] [-ef] [-en] [-dz] [-dy] [-pz] [-py] [-pa] [-pA] [-pb] [-pB] [-pc] [-pC] [-pd] [-pD] [-pe] [-pE] [-pf] [-pF]

Generate random character names

optional arguments:
  -h, --help  show this help message and exit
  -d          Show debug output (DEFAULT: FALSE)
  -n N        Number of names to generate (DEFAULT: 1)

  -o O        Name format. (DEFAULT: 'y z')

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

  -em         Don't use names gendered as male
  -ef         Don't use names gendered as female
  -en         Don't use names gendered as neutral. Ignored by part categories that include gender neutral names

  -dz         Allow duplicate names to appear as family names. This only applies to lists. Will throw an error if you do not have enough unique names.
  -dy         Allow duplicate names to appear as given names. This only applies to lists. Will throw an error if you do not have enough unique names.

  -pz         Print all family list names which fit current gender options
  -py         Print all family list names which fit current gender options

  -pa         Print all given prefixes which fit current gender options
  -pA         Print all given prefixes which fit current gender options or gender neutral options
  -pb         Print all given bases which fit current gender options
  -pB         Print all given bases which fit current gender options or gender neutral options
  -pc         Print all given suffixes which fit current gender options
  -pC         Print all given suffixes which fit current gender options or gender neutral options
  -pd         Print all family prefixes which fit current gender options
  -pD         Print all family prefixes which fit current gender options or gender neutral options
  -pe         Print all family bases which fit current gender options
  -pE         Print all family bases which fit current gender options or gender neutral options
  -pf         Print all family suffixes which fit current gender options
  -pF         Print all family suffixes which fit current gender options or gender neutral options

'''

# Files
This script utilizes two separate files, one for pulling pre-made names, and one for building names from prefixes, bases, and suffixes. Each file is in CSV format.

## Definitions

- PART: This is the text that will be displayed as output.
- KIND: This is the designation for what kinds of names this is used in.
	- z: Family Names, ie "Last Name" (ex: Trebek, Tiger, Beauregarde)
	- y: Given Names, ie "First Name"/"Middle Name(s)" (ex: Alex, Tony, Violet)
	- x: Can be used as either (ex: Thomas, Warren)
- PLACE: Used for generating new names, and designates place within the name. ex name to break down: Hamilton
	- p: Prefix (ex: Ha)
	- b: Base (ex: mil)
	- s: Suffix (ex: ton)
- GENDER: The gender of the name
	- m: masculine (ex: Ivan)
	- f: feminine (ex: Sarah)
	- n: gender neutral (ex: Alex)

It should be noted that the script does not affect the case of any text. If you capitalize the base/suffix or do not capitalize a prefix, those will appear as written (ex: haMilTon).

## build.txt

PART,KIND,PLACE,GENDER

## list.txt

PART,KIND,GENDER

