import re

print("CREATE TABLE species_temp(prefix varchar, name varchar, taxonomy_id varchar, common_name varchar, genus varchar, family varchar, tax_order varchar, tax_class varchar, phylum varchar);")

file1 = open('final_merged.txt', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
for line in Lines:
    values = line.strip().split("\t")
    print('INSERT INTO species_temp(prefix, name, taxonomy_id, common_name, genus, family, tax_order, tax_class, phylum) VALUES ("'+values[0]+'","'+values[1]+'","'+values[2]+'","'+values[3]+'","'+values[4]+'","'+values[5]+'","'+values[6]+'","'+values[7]+'","'+values[8]+'");')

print("CREATE TABLE specimen_temp(taxonomy_id varchar, prefix varchar, public_name varchar, species_name varchar, specimen_id varchar, number integer);")
file1 = open('unique_ids_assigned.txt', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
for line in Lines:
    values = line.strip().split("\t")
    name = values[1]
    name = re.sub(r"^\"",'',name)
    name = re.sub('""','"',name)
    name = re.sub(r"\"$",'',name)
    prefix = re.sub(r"[0-9]+", "", values[0])
    try:
        number = values[3]
    except IndexError:
        number = 1 # To solve problem 7 below
    print('INSERT INTO specimen_temp(prefix, public_name, species_name, specimen_id, number) VALUES ("'+prefix+'","'+values[0]+'",\''+name+'\',"'+values[2]+'",'+str(number)+');')

# Update taxonomy IDs for specimens by prefix.
print("UPDATE specimen_temp SET taxonomy_id = (SELECT taxonomy_id FROM species_temp WHERE species_temp.prefix = specimen_temp.prefix);")

# Problem 1: Duplicate taxonomy IDs
# Solution - remove legacy entries
correct = [(1028678, "Cyrillia aequalis"),
(1036748, "Cylindromonium lichenicola"),
(1036763, "Cylindromonium rhabdosporum"),
(108933, "Myriolecis albescens"),
(108947, "Myriolecis pruinosa"),
(1097674, "Torrentaria lusitanica"),
(1110396, "Pseudosperma curreyi"),
(113330, "Mellicta athalia"),
(1150419, "Gamsomyces longisporus"),
(119176, "Pentanema britannicum"),
(1222197, "Myriolecis andrewii"),
(1222198, "Myriolecis crenulata"),
(1222199, "Myriolecis hagenii"),
(1222200, "Myriolecis semipallida"),
(124277, "Alcyonidium glomeratum"),
(1260805, "Austrosciara hyalipennis"),
(129929, "Platyhypnum smithii"),
(1308814, "Hydroporus figuratus"),
(1336945, "Aka coralliphaga"),
(137456, "Sanguisorba minor"),
(140005, "Hygrohypnella ochracea"),
(140392, "Platyhypnum duriusculum"),
(140393, "Pseudohygrohypnum eugyrium"),
(1449396, "Limacellopsis guttata"),
(156610, "Inosperma cervicolor"),
(1578314, "Hormodochis melanochlora"),
(1593471, "Alloanthostomella rubicola"),
(165590, "Inosperma maculatum"),
(1676542, "Amphorina pallida"),
(171585, "Inachis io"),
(1720519, "Myriolecis sambuci"),
(1738887, "Diaporthe capsici"),
(181928, "Zhuliangomyces illinitus"),
(1821592, "Zhuliangomyces ochraceoluteus"),
(1888684, "Aproaerema albifrontella"),
(207110, "Melinopterus sphacelatus"),
(207139, "Melinopterus consputus"),
(2075506, "Vesiculozygosporium echinosporum"),
(208071, "Curruca cantillans"),
(214181, "Korscheltellus lupulinus"),
(216125, "Steromphala cineraria"),
(217425, "Pseudosperma rimosum"),
(239109, "Mallocybe terrigena"),
(239125, "Inosperma fastigiellum"),
(239126, "Inosperma adaequatum"),
(239127, "Mallocybe agardhii"),
(240311, "Mallocybe heimii"),
(2483277, "Myxarium mesomorphum"),
(279746, "Codonoblepharon forsteri"),
(291647, "Inosperma cookei"),
(295815, "Subcoccinella vigintiquattuorpunctata"),
(29677, "Lolium giganteum"),
(304430, "Hygrohypnella polaris"),
(30804, "Chelon ramada"),
(319549, "Platyhypnum molle"),
(39935, "Myriolecis dispersa"),
(414934, "Phosphuga atrata"),
(419956, "Calvia quattuordecimguttata"),
(445234, "Anemone pulsatilla"),
(455034, "Hypoxylon hinnuleum"),
(4606, "Lolium arundinaceum"),
(461124, "Chlamydosporiella restricta"),
(467841, "Pseudosperma obsoletum"),
(467842, "Pseudosperma perlatum"),
(467843, "Pseudosperma flavellum"),
(467844, "Pseudosperma squamatum"),
(467845, "Pseudosperma mimicum"),
(467887, "Inosperma bongardii"),
(467888, "Inosperma erubescens"),
(467889, "Inosperma quietiodor"),
(470489, "Fraxinicola fraxini"),
(47281, "Edaphochlamys debaryana"),
(478075, "Lewinskya striata"),
(494379, "Roeseliana roeselii"),
(531903, "Pseudoanthostomella conorum"),
(558720, "Propylea quattuordecimpunctata"),
(61563, "Pulvigera lyellii"),
(63592, "Tetraselmis chuii"),
(67002, "Plenogemma phyllantha"),
(674007, "Mallocybe fuscomarginata"),
(685887, "Pseudosperma spurium"),
(692171, "Leobordea lupinifolia"),
(707250, "Alnicola salicis"),
(71488, "Amphorina farrani"),
(72248, "Colias croceus"),
(722662, "Ennomos fuscantarius"),
(875880, "Spilosoma lubricipeda"),
(987418, "Eilema complana"),
(987420, "Eilema griseolum"),
(987424, "Eilema sororcula"),
(987447, "Pterostoma palpinum")]
for pair in correct:
    print("DELETE FROM species_temp where taxonomy_id = "+str(pair[0])+" and name != \""+pair[1]+"\";")

# Problem 2: Some taxonomy IDs are None
# Solution: Remove and add if it ever becomes necessary
print ("DELETE FROM species_temp where taxonomy_id =\"None\";")

# Problem 3: Some public names are duplicated
# Solution: Leave in and ensure API returns correct

# Problem 4: Some prefixes used for specimens are not in the species list
# Solution: update taxonomy IDs from names in these cases (I have checked that there is a 1:1 match)
print("UPDATE specimen_temp SET taxonomy_id = (SELECT taxonomy_id FROM species_temp WHERE species_temp.name = specimen_temp.species_name) where taxonomy_id is null;")

# Problem 5: Species names for some specimens do not match species name
# Solution: Ignore as we will return species name from species table

# Problem 6: Species names are not unique
# Solution: ignore as we are not matching by species name (the time where we did earlier had been checked that there
# was a 1:1 match)

# Problem 7: Some entries in specimens do not have numbers
# Solution: these have been set to one so if a new one comes, 2 will be returned

# Problem 8: Multiple entries with same specimen ID
# Solution: Correct manually
print('DELETE FROM specimen_temp where specimen_id = "SAN0001265" and taxonomy_id = 5802;')
print('DELETE FROM specimen_temp where specimen_id = "SAN0001266" and number = 1;')

# Now create the actual tables
print('CREATE TABLE species (taxonomy_id INTEGER NOT NULL, prefix VARCHAR, name VARCHAR, common_name VARCHAR, genus VARCHAR, family VARCHAR, tax_order VARCHAR, tax_class VARCHAR, phylum VARCHAR, PRIMARY KEY (taxonomy_id));')
print('CREATE TABLE specimen (specimen_id VARCHAR NOT NULL, species_id INTEGER, public_name VARCHAR NOT NULL, number INTEGER NOT NULL, PRIMARY KEY (specimen_id), FOREIGN KEY(species_id) REFERENCES species (taxonomy_id));')

print('INSERT INTO species(taxonomy_id,prefix,name,common_name,genus,family,tax_order,tax_class,phylum) SELECT taxonomy_id,prefix,name,common_name,genus,family,tax_order,tax_class,phylum from species_temp;')
print('INSERT INTO specimen(specimen_id, species_id, public_name, number) select specimen_id, taxonomy_id, public_name, number from specimen_temp;')

#print('DROP TABLE species_temp;')
#print('DROP TABLE specimen_temp;')
