import csv

csvfile = open('../weed_list_2017_02_23.csv', 'rb')
spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

quality = []
for row in spamreader:
    qlt = row[7]
    if qlt.isdigit():
        name = row[12]
    else:
        qlt = row[8]
        name = row[13]
    if qlt=='1' and name[1]=='R':
        quality.append(name)


out = open('unlabeled_quality1.txt','w')
for name in quality:
    out.write(name+'\n')

out.close()
