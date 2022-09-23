# digunakan untuk inisial extraction
import re
import copy 
import random
from .Utils import *

kw_gejala = buka_txt("sfcomp/data/kw_gejala.txt")
kw_obat_2 = buka_txt("sfcomp/data/kw_obat_2.txt")
kw_obat = buka_txt("sfcomp/data/kw_obat.txt")
regex_db = buka_json("sfcomp/data/regex_db.json")

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

    bool_dewasa = re.search("\s*((de?wa?sa?)|(remaja)|(abg))|((umur|usia)\s*((1[3-9])|([2-9][0-9])|(1[0-9][0-9]))\s*(ta?h?u?n))", s, re.IGNORECASE)
    bool_anak = re.search("\s*(ana?k(\s*2|(-|\s*)\s*ana?k))|(ana?k)|((umur|usia)\s*(([2-9])|(1[0-2]))\s*(ta?hu?n))", s, re.IGNORECASE)
    bool_bayi = re.search("\s*(bayi?)|((umur|usia)\s*((([0-9])|([1-4][0-9])|(5[0-2]))\s*minggu))|((umur|usia)\s*((([0-9])|(1[0-2]))\s*bu?la?n))|((umur|usia)\s*((([0-9])|([1-2][0-9]))\s*hari))|(((umur|usia)\s*(((1)|(satu))\s*ta?hu?n)))",s,re.IGNORECASE)

    # dewasa-anak
    if (bool_dewasa):
        exist.append("usia_dewasa")
    elif (bool_anak):
        exist.append("usia_anak")
    elif (bool_bayi) : 
        exist.append("usia_bayi")
    
    # batuk pilek
    if bool(re.search("batuk", s)) and bool(re.search("pilek", s)):
        exist.append("g_batuk_pilek")  
    elif bool(re.search("batuk", s)):
        exist.append("g_batuk")
        unexist.append("pilek")  
    elif bool(re.search("pilek", s)):
        exist.append("pilek")
        unexist.append("batuk")

    #diare 
    if bool(bool_dewasa and re.search("\s*di?a?re",s, re.IGNORECASE)) :
        exist.append("g_diare_dewasa")
    
    #demam
    if bool(re.search("(demam)|(panas)|(h?ang(a|e)t)", s, re.IGNORECASE)):
        exist.append("g_demam")

    # Mencari ket gejala semua gejala
    if(bool_dewasa) :
        cari_ket_diare_dewasa(s, exist, unexist)
    elif (bool_bayi) : 
        cari_ket_demam_bayi(s,exist, unexist)
    elif (bool_anak) : 
        print(f"Fungsi cari ket gejala anak here\n")
    return [id, dialog_status, list(set(exist)), list(set(unexist))]

# Function2 mencari keterangan gejala 
def cari_ket_diare_dewasa (message, exist, unexist) : 
    ket_gejala = ["k_darurat ABCD","k_diare > 14 hari","k_nyeri perut hebat","k_ada drug induced diarhea","k_tinja berdarah/spt cucian beras","k_demam","k_mual muntah","k_dehidrasi"]

    berhenti = False
    i = 1
    while (not berhenti):
        i_str = str(i) 
        try : 
            print(regex_db["diare"]["dewasa"][i_str] == None)
        except KeyError: 
            berhenti = True 
            break
        if(bool(re.search(regex_db["diare"]["dewasa"][i_str],message,re.IGNORECASE))) : 
            exist.append(ket_gejala[i-1])
        i += 1

def cari_ket_demam_bayi(message, exist, unexist) :
    ket_gejala = ["k_usia <3 bulan","k_tdk habis imunisasi","k_suhu >40","k_darurat ABCD","k_priority sign","k_riwayat kejang demam","k_demam >7 hari","k_demam sdh diobati","k_demam blm turun","k_fluktuasi suhu","k_nafas cepat","k_nafas tdk wajar","k_sulit BAK","k_nyeri perut", "k_infeksi","k_lesi lentingan","k_drug induced fever","k_penurunan panas","k_baru imunisasi","k_gigi mau tumbuh", "k_bersin/cairan bening dri hidung/batuk","k_diare","k_ruam", "k_ruam di seluruh tubuh/area wajah", "k_sariawan/tidak mau makan menyusui","k_terbangun di malam/menangis/menarik telinga", "k_tanda gelisah/muntah/nafsu makan hilang/keluar cairan telinga","k_purapura/bintik merah dengue"]

    berhenti = False
    i = 1
    while (not berhenti):
        i_str = str(i) 
        try : 
            print(regex_db["demam"]["bayi"][i_str] == None)
        except KeyError: 
            berhenti = True 
            break
        if(bool(re.search(regex_db["demam"]["bayi"][i_str],message,re.IGNORECASE))) : 
            exist.append(ket_gejala[i-1])
        i += 1
