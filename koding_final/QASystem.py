import QA_Algorithms as algo

# dokumen utama
text = """Ir Soekarno adalah Presiden pertama RI pada periode 1945-1967. Bapak Soekarno lahir di Surabaya, Jawa Timur, 6-Juni-1901. Ir. Soekarno meninggal di Jakarta, 21-Juni-1970 pada umur 69 tahun. Ir. Soekarno adalah Proklamator Kemerdekaan negara Indonesia (bersama dengan Mohammad Hatta) yang terjadi pada tanggal 17-Agustus-1945. Soekarno adalah orang yang pertama kali mencetuskan Pancasila sebagai konsep dasar negara Indonesia dan ia sendiri yang menamainya. Soeharto adalah Presiden kedua RI yang menjabat dari tahun 1967-1998. Soeharto lahir di Yogyakarta, 8-Juni-1921. Soeharto meninggal di Jakarta, 27-Januari-2008 pada umur 86 tahun. Bj. Habibie adalah Presiden ketiga RI. Bj. Habibie lahir di Parepare, Sulawesi Selatan, 25-Juni-1936 Bj. Habibie meninggal di Jakarta, 11-September-2019 pada umur 83 tahun. Bj. Habibie mengundurkan diri dari jabatan presiden pada tanggal 21-Mei-1998"""
print("Text:\n",text,"\n")

# method QASystem -> author: Wilis
def getAnswer(question, text):                                          # input: pertanyaan, dan data teks
    print("Question:\n",question,"\n")                                  # tampilkan pertanyaan
    keyword, tag_search, verba = algo.question_processor(question)      # lakukan question processing
    passage = algo.passage_retieval(text, keyword)                      # lakukan passage retrieval
    print("relevant passage:\n",passage[0],"\n")                        # tampilkan relevant passage (dokumen yang cocok dengan pertanyaan)
    answer = algo.answer_processor(passage, tag_search, verba)          # lakukan answer processing
    print("system answer\t: ",answer)                                   # tampilkan jawaban dari QAS
    return answer                                                       # mengembalikan nilai answer

# method akurasi -> author: Wilis
def getAkurasi(realAnswer, systemAnswer):                               # input: jawaban asli, dan jawaban dari sistem
    realAnswer = realAnswer.split(" ")                                  # memecah jawaban asli menjadi per kata
    systemAnswer = systemAnswer.split(" ")                              # memecah jawaban dari sistem menjadi per kata
    akurasi = 0                                                         # menginisialisasi nilai awal akurasi
    for answer in systemAnswer:                                         # looping tiap kata pada jawaban sistem
        if answer in realAnswer:                                        # jika: kata terdapat pada jawaban asli
            akurasi += 1                                                # maka: nilai akurasi ditambah 1
    akurasi /= len(realAnswer) * 0.01                                   # nilai akhir akurasi -> maksimal 100
    if akurasi>=75:                                                     # jika: akurasi lebih dari atau sama dengan 75
        b_s = '"BENAR"'                                                 # maka: jawaban dinyatakan benar
    else: b_s = '"SALAH"'                                               # selain itu: maka jawaban dinyatakan salah
    print("real answer\t\t: ", " ".join(realAnswer))                    # tampilkan jawaban asli
    print("akurasi\t\t\t: ", akurasi, " %")                             # tampilkan nilai akurasi
    print("Jawaban ",b_s)                                               # tampilkan kebenaran jawaban
    print("\n#################################################\n")      # pembatas
    return akurasi                                                      # mengembalikan nilai akurasi

# penyimpanan nilai akurasi
akurasi = []

# pertanyaan 1
q = "Siapa presiden pertama RI?"
r_a = "Soekarno"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 2
q = "Kapan Soekarno menjadi presiden?"
r_a = "1945-1967"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 3
q = "Dimana Soekarno lahir?"
r_a = "Surabaya"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 4
q = "Kapan Soekarno meninggal?"
r_a = "21 Juni 1970"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 5
q = "Siapa proklamator kemerdekaan negara Indonesia?"
r_a = "Soekarno dan Mohammad Hatta"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 6
q = "Konsep apa yang dicetuskan oleh Soekarno sebagai dasar negara?"
r_a = "Pancasila"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 7
q = "Soeharto adalah presiden RI yang ke berapa?"
r_a = "kedua"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 8
q = "Dimana Soeharto meninggal?"
r_a = "Jakarta"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 9
q = "pada umur berapa Bj. Habibie meninggal?"
r_a = "83 tahun"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# pertanyaan 10
q = "Kapan negara Indonesia merdeka?"
r_a = "17 Agustus 1945"
a = getAnswer(q,text)
akurasi.append(getAkurasi(r_a, a))

# rata - rata akurasi
jumlah_akurasi = 0
for nilai in akurasi:
    jumlah_akurasi += nilai
rata_rata_akurasi = jumlah_akurasi/len(akurasi)
print("rata-rata akurasi: ", rata_rata_akurasi, " %")