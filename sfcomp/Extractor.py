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

    bool_dewasa = re.search("\s*de?wa?sa?", s, re.IGNORECASE)
    bool_anak = re.search("\s*(ana?k(\s*2|(-|\s*)\s*ana?k))", s, re.IGNORECASE)
    bool_bayi = re.search("\s*bayi",s,re.IGNORECASE)

    # dewasa-anak
    if (bool_dewasa):
        exist.append("usia_dewasa")
    elif (bool_anak):
        exist.append("usia_anak")
    elif (bool_bayi) : 
        exist.append("usia_bayi")
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
    if bool(re.search("\s*di?a?re",s, re.IGNORECASE)) :
        exist.append("diare")
        

    # Mencari ket gejala semua gejala
    if(bool_dewasa) :
        cari_ket_diare_dewasa(s, exist, unexist)
    elif (bool_bayi) : 
        cari_ket_demam_bayi(s,exist, unexist)
    elif (bool_anak) : 
        print(f"Fungsi cari ket gejala anak here\n")
    return [id, dialog_status, list(set(exist)), list(set(unexist))]


# Function2 keterangan gejala 
# def ket_diare(message, exist, unexist) :
#     print(print)

# Function2 mencari keterangan gejala 
def cari_ket_diare_dewasa (message, exist, unexist) : 
    pattern = ["\s*(ta?nda?)?\s*((ke)?ga?wa?td?a?r?u?r?a?(ta?n)?)?\s*ABCD","\s*((d(a|i)(i|a)re)\s*(((1[5-9])|([2-9][0-9]))\s*ha?ri?))|((d(a|i)(i|a)re)\s*(le?bi?h)\s*(da?ri?)?\s*14\s*ha?ri?)|((d(a|i)(i|a)re)\s*14\s*(ha?ri?)\s*(le?bi?h))","((pe?ru?t)\s*((sa?ki?t)|(nye?ri))\s*((pa?ra?h)|(he?ba?t)|(se?ka?li?)|(kro?ni?s)|(ba?n?ge?t)))","\s*((obat)\s*(pemicu))|(dru?g\s*indu?ce?d\s*diarh?e?a)|(((obat)|(pil)|(kapsul)(tablet)))","\s*(((ti?nja?)|(fe?se?s)|(be?ra?k)|(bab))\s*((\w)*)?\s*(be?r)?da?ra?h)|(((\w)*)?\s*(be?r)?da?ra?h\s*((\w)*)?\s*((ti?nja?)|(fe?se?s)|(be?ra?k)|(bab)))|(((ti?nja?)|(fe?se?s)|(be?ra?k)|(bab))\s*cu?ci?a?n\s*be?ra?s)|(cu?ci?a?n\s*be?ra?s)","\s*(de?ma?m|me?ri?a?ng|ge?ra?h|pa?na?s|palak)","\s*(mual|muntah)","\s*((dahaga|haus)\s*(se?kali|ba?nge?t|pa?ra?h))|(dehidra?si?)|(urine?\s*?ge?la?p)|(ge?la?p\s*?\s*urine?)|(ku?li?t\s*(ke?ri?ng|ga?ri?ng))"]

    ket_gejala = ["darurat ABCD","diare > 14 hari","nyeri perut hebat","ada drug induced diarhea","tinja berdarah/spt cucian beras","demam","mual muntah","dehidrasi"]

    i = 0
    while (i <= len(pattern) -1 ) : 
        if(bool(re.search(pattern[i],message,re.IGNORECASE))) : 
            exist.append(ket_gejala[i])
        # else : 
        #     unexist.append(ket_gejala[i])
        
        i += 1

def cari_ket_demam_bayi(message, exist, unexist) :
    pattern = ["\s*((usia|umu?r)\s*(([0-2]\s*(bu?la?n))|(([1-9]|1[0-1])\s*minggu)))\s*(\w)*\s*((ti?da?k)|(e?n?gg?ak?)|(be?lu?m))\s*(\w)*\s*imunisa?si?","\s*((suhu|te?mpe?ra?tu?re?)\s*(((4[1-9])|([5-9][0-9]))\s*(de?ra?ja?t)?))|((suhu|te?mpe?ra?tu?re?)\s*(le?bi?h|le?wa?t)\s*(da?ri?)?\s*40\s*(de?ra?ja?t)?)|((suhu|te?mpe?ra?tu?re?)\s*40\s*(de?ra?ja?t)?\s*(le?bi?h|le?wa?t))","\s*((ta?nda?)|sign)?\s*((((ke)?ga?wa?td?a?r?u?r?a?((ta?n)|(t))?)?)|(eme?rge?ncy?)?)\s*ABCD","\s*(((pri?o?ri?t(y|i))\s*((ta?nda?)|sign)?)|(((ta?nda?)|sign)\s*(priorit(y|i)))\s*)|(((\w)*)\s*3tpr mob)","\s*((ri?wa?ya?t|histor(i|y)?)?\s*(ke?ja?n?g)\s*(de?ma?m))|((ri?wa?ya?t|histor(i|y)?)?\s*(de?ma?m)\s*(ke?ja?n?g))","\s*(((de?ma?m|pa?na?s|meriang|ge?ra?h)\s*((([8-9])|([1-9][0-9]))\s*(ha?ri?)?))|((de?ma?m|pa?na?s|meriang|ge?ra?h)\s*(le?bi?h|le?wa?t)\s*(da?ri?)?\s*7\s*(ha?ri?)?)|((de?ma?m|pa?na?s|meriang|ge?ra?h)\s*7\s*(ha?ri?)?\s*(le?bi?h|le?wa?t)))\s*\w*\s*(be?lu?m|ti?da?k|e?n?g?ga?k?)\s*((\w)*\s)*((me)?(t|n)u?ru?n)\s*((suhu)|(panas)|(demam))?","\s*(((suhu?)|(te?mpe?ra?tu?re?))\s*((\w)*)?)\s*(((naik\s*turun)|(turun\s*naik)|(fluktuatif)|((ti?da?k)|(e?n?g?gak?)\s*stabil))|((ka?da?n?g)\s*(naik|turun)\s*(ka?da?n?g)\s*(naik|turun)))","\s*(((na?(f|p)a?s))\s*(((su?sa?h)|(su?li?t)|(ce?pa?t)|(laju))|(((ti?da?k)|(e?n?gg?ak?))\s*((wa?ja?r)|(no?rma?l)|(bia?sa)))))|((((su?sa?h)|(su?li?t)|(ce?pa?t)|(laju))|(((ti?da?k)|(e?n?gg?ak?))\s*((wa?ja?r)|(no?rma?l)|(bia?sa))))\s*((na?(f|p)a?s)))","\s*(((su?li?t)|(su?sa?h))\s*((bak)|(buang air ke?ci?l)|(ke?nci?n?g)|(pi?pi?s)))|(((bak)|(buang air ke?ci?l)|(ke?nci?n?g)|(pi?pi?s))\s*((su?li?t)|(su?sa?h)))","\s*((pe?ru?t)\s*((sa?ki?t)|(nye?ri))\s*)|(((sa?ki?t)|(nye?ri))\s*(pe?ru?t)\s*)"]

    ket_gejala = ["usia <3 bulan & tdk habis imunisasi","suhu >40","darurat ABCD","priority sign","riwayat kejang demam","demam >7 hari & blm turun","fluktuasi suhu","nafas cepat","sulit BAK","nyeri perut"]

    i = 0
    while (i <= len(pattern) -1 ) : 
        if(bool(re.search(pattern[i],message,re.IGNORECASE))) : 
            exist.append(ket_gejala[i])
        # else : 
        #     unexist.append(ket_gejala[i])
        
        i += 1
    



#Apakah ada tanda kegawatdaruratan ABCD?
# Apakah diare berlangsung >14 hari?
# Apakah ada nyeri perut hebat?
# Apakah ada pemicu obat (drug induced diarhea)
# Apakah tinja ada darah atau seperti air cucian beras?
# Apakah ada demam?
