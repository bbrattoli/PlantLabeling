import csv
import numpy as np
import os

files = os.listdir('images')

csvfile = open('../weed_list_2017_02_23.csv', 'rb')
spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

names = []
quality = []
for row in spamreader:
    qlt = row[7]
    if qlt.isdigit():
        name = row[12]
    else:
        qlt = row[8]
        name = row[13]
    if name in files:
        quality.append(int(qlt))
        names.append(name)

quality = np.asarray(quality)
names = np.asarray(names)
names = names[quality==1]

out = open('unlabeled_quality1.txt','w')
for name in names:
    out.write(name+'\n')

out.close()
