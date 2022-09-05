import re
import ast
import random
from sfcomp.Utils import *
from sfcomp.Extractor import extractor

kw_gejala = buka_txt("sfcomp/data/kw_gejala.txt")
kw_obat_2 = buka_txt("sfcomp/data/kw_obat_2.txt")
kw_obat = buka_txt("sfcomp/data/kw_obat.txt")
db_batuk = buka_json("sfcomp/data/db_batuk.json")

dialog = {
    "t_dewasa_anak": ["Pasiennya dewasa atau masih anak-anak?", "Baik, sudah kami catat. Dewasa atau anak ya?"],
    "t_batuk_rec_dewasa": ["Berikan obat batuk pilek dan sarankan ke dokter untuk meresepkan antibiotik"],
    "t_batuk_rec_anak":["Berikan terapi suportif non farmakologi yang bisa mengurangi batuk atau pilek (misalnya balsem transpulmin). Jika tidak berkurang diperiksakan ke dokter"],
    "t_tidak_tahu":["Mohon maaf, saya tidak paham, bisa diulangi lagi?", "Maaf, apakah bisa diulang?"]
}

pertanyaan = {
    "p_diare_dewasa" : ["Apakah ada tanda kegawatdaruratan ABCD?","Apakah diare berlangsung >14 hari?","Apakah ada nyeri perut hebat?","Apakah ada pemicu obat (drug induced diarhea)","Apakah tinja ada darah atau seperti air cucian beras?","Apakah ada demam?","Apakah ada mual muntah?","Apakah ada tanda /gejala dehidrasi"],
    
    "p_demam_bayi": ["Kemungkinan infeksi. Sarankan ke dokter untuk mendapatkan resep antibiotik","Kemungkinan Herpes Simpleks sarankan ke dokter untuk mendapatkan resep antivirus lain.",
    "Penghentian obat (drug induced fever) akan mengembalikan suhu tubuh dalam 72 jam", "Berikan antipiretik yang lain (parasetamol atau ibuprofen)",
    "Menurunkan dengan kompres hangat atau antipiretik 10-15 mg/kgBB atau parasetamol diikuti kompres hangat 1 jam setelah antipiretik",
    "Menurunkan temperatur anak dengan kompres hangat atau parasetamol", "Lanjut ke pertanyaan terkait gejala batuk pilek", "Lanjut ke pertanyaan terkait gejala diare",
    "lanjut pert 9", "Ada kemungkinan cacar air/varisela atau campak, berikan parasetamol, tanpa penyulit, bisa sembuh sendiri (self limiting disease). Asiklovir efektif mempercepat durasi jika diberikan <24 jam",
    "Ada kemungkinan flu singapura, berikan parasetamol dan krim antigatal, atau tablet hisap antiseptik mulut, tanpa penyulit, bisa sembuh sendiri (self limiting disease)",
    "Kemungkinan Otitis Media, lanjutkan ke prt 23", "Kemungkinan Otitis Media tingkat lanjut, sarankan ke dokter untuk mendapatkan antibiotik", "Sarankan bedrest, paracetamol, minum yang banyak, jus jambu biji, cek trombosit atau gejala perdarahan hingga hari ke 5" ]
}

gejala = {
    "g_diare_dewasa": ["k_darurat ABCD","k_diare > 14 hari","k_nyeri perut hebat","k_ada drug induced diarhea","k_tinja berdarah/spt cucian beras","k_demam","k_mual muntah","k_dehidrasi"]
}

def cek_batuk(s):
    return bool(re.search("batuk", s))
        
def cek_anak(s):
    return bool(re.search("anak", s))  

def cek_dewasa(s):
    return bool(re.search("(dewasa)|(tua)|((1[8-9])|([2-9][0-9]) ta?hu?n)",s)) # > 18 tahun

# Mencari gejala diare dewasa dan indeks terbesar keterangan gejalanya
def cari_data_diare_dewasa(gejala_found) :
    indeks_terbesar = 0
    for i in range(0, len(gejala_found)):
        gejala_pasien = gejala_found[i]
        for k in range(0, len(gejala["g_diare_dewasa"])):
            ket_gejala =  gejala["g_diare_dewasa"][k]
            if(gejala_pasien == ket_gejala) : 
                indeks_terbesar = k

    return indeks_terbesar

# Mengembalikan pertanyaan2 utk mencari data gejala diare dewasa
def tanya_diare_dewasa (indeks) :
    hasil_indeks = 0

    for i in range(indeks, 1): 
        hasil_indeks = i
    
    hasil_pertanyaan = pertanyaan["p_diare_dewasa"][hasil_indeks] 
    return hasil_pertanyaan
        
# def cek_diare(s)

# s = pesan
def main_checker(s, user_session_id=None, user_note=None):
    
    print(f"user session id ={user_session_id}\n")
    print(f"user note atas ={user_note}\n")
    print(f"pesan (s) ={s}\n")

    if user_note == None:
        user_note = {"gejala_tidak":[], "gejala_ada":[]}
    else:
        user_note = ast.literal_eval(user_note)

    gejala_tidak = user_note["gejala_tidak"]
    gejala_ada = user_note["gejala_ada"]
    med_rec = [user_session_id, 0, gejala_ada, gejala_tidak]
    print(f"med rec sebelum extractor: {med_rec}\n")

    # update gejala
    med_rec = extractor(s, med_rec)

    gejala_ada_list = med_rec[2]
    
    print(f"med rec setelah extractor: {med_rec}\n")
    print(f"med_rec[2] = {med_rec[2]}")

    # if cek_batuk(s) and not(cek_dewasa(s) or cek_anak(s)):
    #     return random.choice(dialog["t_dewasa_anak"])
    # if (cek_batuk(s) and cek_dewasa(s)) or cek_dewasa(s):
    #     return random.choice(dialog["t_batuk_rec_dewasa"])
    # if (cek_batuk(s) and cek_anak(s)) or cek_anak(s):
    #     return random.choice(dialog["t_batuk_rec_anak"])
    # return random.choice(dialog["t_tidak_tahu"])

    user_note = {"gejala_ada": med_rec[2], "gejala_tidak": med_rec[3]}
    print(f"user note bawah ={user_note}\n")

    indeks =cari_data_diare_dewasa(gejala_ada_list)
    hasil_pertanyaan = tanya_diare_dewasa(indeks)

    return hasil_pertanyaan, str(user_note)

# TEST
# main_checker("ada orang dewasa batuk", 1)
