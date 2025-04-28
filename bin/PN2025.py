import os

if os.name == 'nt':  # Windows
    percorso_file = 'log\\'
    DBdir = 'db\\'
else:  # Linux/Mac
    percorso_file = 'log/'
    DBdir = 'db/'

AAA = []

f = open(DBdir+'AAA.txt', 'r')
righe = f.readlines()
for riga in righe:
    riga = riga.replace('\n','')
    AAA.append(riga.split(','))
f.close()   