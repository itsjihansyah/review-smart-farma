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

    return [id, dialog_status, list(set(exist)), list(set(unexist))]