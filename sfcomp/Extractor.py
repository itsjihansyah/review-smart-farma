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
    pattern = ["\s*(ta?nda?)?\s*((ke)?ga?wa?td?a?r?u?r?a?(ta?n)?)?\s*ABCD",
    "\s*((d(a|i)(i|a)re)\s*((((1[5-9])|([2-9][0-9]))\s*ha?ri?)|(([1-9])|([1-9][0-9]))\s*bu?la?n))|((d(a|i)(i|a)re)\s*((le?bi?h)\s*(da?ri?)?|>)\s*((((14)|(1[5-9])|([2-9][0-9]))\s*ha?ri?)|((([2-9])|([1-9][0-9]))\s*mi?nggu)|((([1-9])|([1-9][0-9]))\s*bu?la?n)))|((d(a|i)(i|a)re)\s*14\s*(ha?ri?)\s*(le?bi?h))|((d(a|i)(i|a)re)\s*((((1[5-9])|([2-9][0-9]))\s*ha?ri)|((([3-9])|([1-9][0-9]))\s*mi?nggu)))"
    ,"\s*(((sa?ki?t)|(nye?ri))\s*pe?ru?t\s*((pa?ra?h)|(he?ba?t)|(se?ka?li?)|(kro?ni?s)|(ba?n?ge?t)))|((pe?ru?t)\s*((sa?ki?t)|(nye?ri))\s*((pa?ra?h)|(he?ba?t)|(se?ka?li?)|(kro?ni?s)|(ba?n?ge?t)))"
    ,"\s*(((obat)|(pil)|(kapsul)|(tablet))\s*(pemicu))|(dru?g\s*indu?ce?d\s*diarh?e?a)|(((selesai)|(ha?bi?s))\s*((minum)|((t|n)e?la?n))\s*((obat)|(pil)|(kapsul)|(tablet)))"
    ,"\s*((da?ra?h(\w)*)\s*((((pada)|(di))?\s*((tinja)|(berak)|(feses)))|(((saat)|(ketika)|(saat)|(pas))\s*((berak)|(bab)|(buang air besar)|(ngengek)))))|(((tinja)|(bab)|(berak)|(feses))\s*(\w)*\s*da?ra?h)|(((tinja)|(bab)|(berak)|(feses))\s*((\w)*\s*)*cucian\s*be?ra?s)"
    ,"\s*((\S|\s)*)+(de?ma?m|me?ri?a?ng|ge?ra?h|pa?na?s|palak)"
    ,"\s*((mual)\s*(\w)*\s*(muntah))|((muntah)\s*(\w)*\s*(mual))"
    ,"\s*(dahaga|haus)\s*((se?kali|ba?nge?t|pa?ra?h))|(urine?((\w|\s)*)?ge?la?p)|(ge?la?p\s*((\w)*)?\s*urine?((\w)*)?)|(ku?li?t((\w|\s)*)?(ke?ri?ng|ga?ri?ng))|(((gejala)|(tanda)|(sign))\s*dehidrasi)"]

    ket_gejala = ["k_darurat ABCD","k_diare > 14 hari","k_nyeri perut hebat","k_ada drug induced diarhea","k_tinja berdarah/spt cucian beras","k_demam","k_mual muntah","k_dehidrasi"]

    i = 0
    while (i <= len(pattern) -1 ) : 
        if(bool(re.search(pattern[i],message,re.IGNORECASE))) : 
            exist.append(ket_gejala[i])
        # else : 
        #     unexist.append(ket_gejala[i])
        
        i += 1

def cari_ket_demam_bayi(message, exist, unexist) :
    pattern = ["\s*((usia|umu?r)\s*(([0-2]\s*(bu?la?n))|(([1-9]|1[0-1])\s*minggu)))"
    ,"\s*((ti?d?a?k)|(e?n?gg?ak?)|(be?lu?m))\s*(\w)*\s*imunisa?si?"
    ,"\s*((suhu|te?mpe?ra?tu?re?)\s*(((4[1-9])|([5-9][0-9]))\s*(de?ra?ja?t)?))|((suhu|te?mpe?ra?tu?re?)\s*(le?bi?h|le?wa?t|>)\s*(da?ri?)?\s*(40|empa?t\s*pu?lu?h)\s*(de?ra?ja?t)?)|((suhu|te?mpe?ra?tu?re?)\s*40\s*(de?ra?ja?t)?\s*(le?bi?h|le?wa?t))"
    ,"\s*((ta?nda?)|sign)?\s*((((ke)?ga?wa?td?a?r?u?r?a?((ta?n)|(t))?)?)|(eme?rge?ncy?)?)\s*ABCD"
    ,"\s*(((pri?o?ri?t(y|i))\s*((ta?nda?)|sign)?)|(((ta?nda?)|sign)\s*(priorit(y|i)))\s*)|(((\w)*)\s*3tpr mob)"
    ,"\s*((ri?wa?ya?t|histor(i|y)?|sejarah|catatan)\s*(ke?ja?n?g)\s*(de?ma?m))|((ri?wa?ya?t|histor(i|y)?|sejarah|catatan)?\s*(de?ma?m)\s*(ke?ja?n?g))"
    ,"\s*(((de?ma?m|pa?na?s|meriang|ge?ra?h)\s*((((([8-9])|([1-9][0-9]))\s*(ha?ri?))|(([2-9])|([1-9][0-9]))\s*mi?n?ggu?)|(\s*(le?bi?h|le?wa?t)\s*(da?ri?)?\s*((7\s*(ha?ri?))|((1)|(satu))\s*mi?n?ggu?))|(\s*((7\s*(ha?ri?))|((1)|(satu))\s*mi?n?ggu?)\s*(le?bi?h|le?wa?t))|((>)\s*((7\s*(ha?ri?))|((1)|(satu))\s*mi?n?ggu?)))))"
    ,"\s*(be?lu?m|ti?d?a?k|e?n?g?ga?k?)\s*((\w)*\s)*((me)?(t|n)u?ru?n)\s*((suhu)|(temperature?)|(pa?na?s)|(de?ma?m))"
    ,"\s*(((suhu?)|(te?mpe?ra?tu?re?))\s*((\w)*)?)\s*(((naik\s*turun)|(turun\s*naik)|(fluktuatif)|((ti?da?k)|(e?n?g?gak?)\s*stabil))|((ka?da?n?g)\s*(naik|turun)\s*(ka?da?n?g)\s*(naik|turun)))"
    ,"\s*((na?(f|p)a?s\w*)\s*\w*\s*((ce?pa?t)|(laju)))|(((ce?pa?t)|(laju))\s*\w*\s*(na?(f|p)a?s\w*))"
    ,"\s*(((na?(f|p)a?s))\s*\w*\s*\w*\s*((((ti?d?a?k)|(e?n?gg?ak?))\s*((wa?ja?r)|(no?rma?l)|(bia?sa)))))|(((((ti?d?a?k)|(e?n?gg?ak?))\s*((wa?ja?r)|(no?rma?l)|(bia?sa))))\s*((na?(f|p)a?s)))"
    ,"\s*(((su?li?t)|(su?sa?h))\s*((bak)|(buang air ke?ci?l)|(ke?nci?n?g)|(pi?pi?s)))|(((bak)|(buang air ke?ci?l)|(ke?nci?n?g)|(pi?pi?s))\s*((su?li?t)|(su?sa?h)))"
    ,"\s*((pe?ru?t)\s*\w*\s*((sa?ki?t)|(nye?ri)|(pe?rih))\s*)|(((sa?ki?t)|(nye?ri)|(pe?rih))\s*(pe?ru?t)\s*)"
    ,"\s*((in(f|v)eksi)|dahak|(ber)*?ingus(( kuning| bewarna| *warna)))"
    ,"\s*((lesi|lenting(an)?)|(se?pe?rti? her(v|p)es))"
    ,"\s*((obat pemicu( demam|pa?na?s|h?ang(a|e)t)?)|(drug induced fever))"
    ,"\s*((pen|t)urun((an)?)|(turun naik)|(naik turun))"
    ,"\s*((h?abis|baru )?(di ?)?(imunisasi))"
    ,"\s*((gigi)( *baru? mau|akan tumbuh)?)",
    "\s*(bersin|flu|cairan( bening)?|ba?tuk|hidung)"
    ,"\s*((diare)|(se?ring (bab|buang air)))"
    ,"\s*((ruam)|kulit( ga?t(a|e)?l|iritasi|me?ra?h|ruam)|(ga?t(a|e)?l|iritasi|me?ra?h|ruam)( *kulit))"
    , "\s*((ruam)|kulit( ga?t(a|e)?l|iritasi|me?ra?h|ruam) di( ?se?lu?ru?h tu?bu?h| *wajah))"
    ,"\s*(b(i|e)nt(i|o)l)|(sariawan)|((tidak|e?n?g?ga?k?) ?)m(au|o) (makan|menyusui)","\s*((ter)?bangun)*malam|(me)?nangis|((me)?narik)*telinga"
    ,"\s*(gelisah|muntah|cairan)|(((tidak|e?n?g?ga?k?) )?nafsu( *hilang)?)|(cairan (telinga|kuping))"
    ,"\s*((pura*(pura)?)|(binti(k|l)*merah)|(dengue))"]

    ket_gejala = ["k_usia <3 bulan"
    ,"k_tdk habis imunisasi"
    ,"k_suhu >40"
    ,"k_darurat ABCD"
    ,"k_priority sign"
    ,"k_riwayat kejang demam"
    ,"k_demam >7 hari"
    ,"k_demam_blm turun"
    ,"k_fluktuasi suhu"
    ,"k_nafas cepat"
    ,"k_nafas tidak wajar"
    ,"k_sulit BAK"
    ,"k_nyeri perut"
    ,"k_infeksi"
    ,"k_lesi lentingan"
    ,"k_obat pemicu demam rutin sebulan"
    ,"k_terjadi penurunan panas"
    ,"k_baru diimunisasi"
    ,"k_gigi mau tumbuh"
    ,"k_disertai bersin, cairan bening dri hidung, atau batuk","k_ada diare"
    ,"k_ruam"
    ,"k_ruam di seluruh tubuh/area wajah"
    ,"k_bintil/sariawan/tidak mau makan menyusui"
    ,"k_terbangun di malam, menangis, menarik telinga"
    ,"k_tanda gelisah, muntah, nafsu makan hilang, keluar cairan telinga"
    ,"k_purapura/bintik merah dengue"]

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
