import re

def escape(val):
    val = re.sub('\'','\'\'',val)
    return val

file1 = open('additions.txt', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
print('BEGIN;')
for line in Lines:
    values = line.strip().split("\t")
    print('INSERT INTO species(prefix, name, taxonomy_id, common_name, genus, family, tax_order, tax_class, phylum) VALUES (\''+escape(values[0])+'\',\''+escape(values[1])+'\','+values[2]+',\''+escape(values[3])+'\',\''+escape(values[4])+'\',\''+escape(values[5])+'\',\''+escape(values[6])+'\',\''+escape(values[7])+'\',\''+escape(values[8])+'\');')
print('COMMIT;')


