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
    "t_tidak_tahu":["Mohon maaf, saya tidak paham, bisa diulangi lagi?", "Maaf, apakah bisa diulang?"],

    # NABILS
    "t_batuk" : ["Berikan obat batuk pilek dan sarankan ke dokter untuk meresepkan antibiotik"],
}

def cek_batuk(s):
    return bool(re.search("batuk", s))
        
def cek_anak(s):
    return bool(re.search("anak", s))        

def cek_dewasa(s):
    return 

# s = pesan
def main_checker(s, user_session_id=None, user_note=None):
    
    print(f"user session id ={user_session_id}")
    print(f"user note ={user_note}")
    print(f"s ={s}")

    print("HALOOOOOOOOOO")
    if user_note == None:
        print("KESINI")
        user_note = {"gejala_tidak":[], "gejala_ada":[]}
    else:
        user_note = ast.literal_eval(user_note)

    gejala_tidak = user_note["gejala_tidak"]
    gejala_ada = user_note["gejala_ada"]
    med_rec = [user_session_id, 0, gejala_ada, gejala_tidak]

    # update gejala
    med_rec = extractor(s, med_rec)
    
    print(f"med_rec = {med_rec}")
    
    # if cek_batuk(s) and not(cek_dewasa(s) or cek_anak(s)):
    #     return random.choice(dialog["t_dewasa_anak"])
    # if (cek_batuk(s) and cek_dewasa(s)) or cek_dewasa(s):
    #     return random.choice(dialog["t_batuk_rec_dewasa"])
    # if (cek_batuk(s) and cek_anak(s)) or cek_anak(s):
    #     return random.choice(dialog["t_batuk_rec_anak"])
    # return random.choice(dialog["t_tidak_tahu"])

    user_note = {"gejala_ada": med_rec[2], "gejala_tidak": med_rec[3]}
    # print(f'user_note {str(user_note)}')
    
    # NABILS
    if (cek_batuk(s)) :
        return dialog["t_batuk"][0], str(user_note)

    return "kamu sakit", str(user_note)

# TEST
# main_checker("ada orang dewasa batuk", 1)