import hashlib
import itertools
import string

file = input("Enter filename: ")

f1=open(file, 'w+')

num = '0123456789'
a_z = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numAZ = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
top = "https://applyonlinenow.com/USCCapp/Ctl/entry?sc="
prefixes = ["VAA","VAB","FAA","FAB","FAC","UAA","UAB","UAC","BAC","BAB"]
#top =  "https://applynow.chase.com/FlexAppWeb/renderApp.do?SPID=F"
bottom = ""
for prefix in prefixes:
	for (a) in map(''.join, itertools.product(a_z, repeat=3)):
	#for (b) in itertools.imap(''.join, itertools.product(numAZ, repeat=2)):
		f1.write(top + prefix)
		f1.write(''.join(a))
		f1.write('\n')