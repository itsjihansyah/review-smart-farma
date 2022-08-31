# digunakan untuk inisial extraction
import re
import copy 
import random
from .Utils import *

kw_gejala = buka_txt("sfcomp/data/kw_gejala.txt")
kw_obat_2 = buka_txt("sfcomp/data/kw_obat_2.txt")
kw_obat = buka_txt("sfcomp/data/kw_obat.txt")

# convert list kw_gejala to dict
gejala_dict = {}
for i, kw in enumerate(kw_gejala):
    gejala_dict[kw] = i

def extractor(s, med_rec):
    exist = []
    unexist = []
    id = med_rec[0]
    dialog_status = med_rec[1]
    if med_rec[2]!=None:
        exist = med_rec[2]

    # dewasa-anak
    if bool(re.search("dewasa", s)):
        exist.append("usia_dewasa")
    elif bool(re.search("anak", s)):
        exist.append("usia_anak")
    
    # demam
    if bool(re.search("demam", s)):
        exist.append("demam")
    
    # batuk pilek
    if bool(re.search("batuk", s)) and bool(re.search("pilek", s)):
        exist.append("batuk_pilek")  
    elif bool(re.search("batuk", s)):
        exist.append("batuk")
        unexist.append("pilek")  
    elif bool(re.search("pilek", s)):
        exist.append("pilek")
        unexist.append("batuk")

    #diare 
    if bool(re.search("\s*di?a?re",s)) :
        exist.append("diare")
        ket_diare()

    return [id, dialog_status, list(set(exist)), list(set(unexist))]


# Function2 keterangan gejala 
def ket_diare(message) :
    print(print)

# Function2 mencari keterangan gejala 
def cari_ket_diare (message) : 
    pattern = ["\s*(ta?nda?)?\s*((ke)?ga?wa?td?a?r?u?r?a?(ta?n)?)?\s*ABCD","\s*((sa?ki?t)|(nye?ri))\s*pe?ru?t\s*((pa?ra?h)|(he?ba?t)|(se?ka?li?))"]



#Apakah ada tanda kegawatdaruratan ABCD?
# Apakah diare berlangsung >14 hari?
# Apakah ada nyeri perut hebat?
# Apakah ada pemicu obat (drug induced diarhea)
# Apakah tinja ada darah atau seperti air cucian beras?
# Apakah ada demam?
