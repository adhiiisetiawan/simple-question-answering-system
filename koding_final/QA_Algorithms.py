# import
import nltk
from nltk.tag import CRFTagger
from nltk.tag.stanford import StanfordNERTagger
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import os
import re

########################################################################################################################
# pos_tagger -> author: Adhi, Tuahta
def pos_tagger(text):                   # input: teks/String
    # instansiasi
    ct = CRFTagger()

    # load model tagger indonesia
    ct.set_model_file('model_postagging_crf.tagger')

    # cleaning
    text = re.sub('\.?\,?\(?\)?\"?', '', text)
    text = re.sub("\n", " ", text)
    text = text.split(" ")

    # ini fungsi untuk melakukan postagging
    tagged_text = ct.tag_sents([text])

    # hasil
    return tagged_text                  # output: teks yang sudah diberi pos_tag
# run pos_tagger
# teks = 'Ani pergi untuk membeli bunga seharga 5000 rupiah.'
# tagged_teks = pos_tagger(teks)
# print (tagged_teks)
# end postagger

########################################################################################################################
# ner_tagger -> author: Adhi, Giffaro
def ner_tagger(text):                       # input: teks/String
    # setting java
    java_path = "C:/Program Files/Java/jdk1.8.0_171/bin/java.exe"
    os.environ['JAVAHOME'] = java_path

    # file jar dibutuhkan untuk stanford. sesuaikan dg direktori tempat menyimpan file library stanford
    jar = 'stanford-ner/stanford-ner.jar'

    # load model sesuaikan dg direktori tempat menyimpan file library stanford
    model = 'stanford-ner/ner-model-indonesian.ser.gz'

    # bagian ini digunakan untuk nyiapin NER tagger pake bahsa indonesia
    ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

    # tokenisasi
    text = re.sub('\.?\,?\(?\)?\"?', '', text)
    text = nltk.word_tokenize(text)

    # Run NER tagger
    ner_text = ner_tagger.tag(text)

    #hasil
    return ner_text                 # output: teks yang sudah diberi ner_tag
# run ner_tagger
# teks = "Budi mambagikan sepeda motor di kota Jakarta seharga 3 juta rupiah."
# ner_teks = ner_tagger(teks)
# print(ner_teks)
# end ner_tagger

########################################################################################################################
# stemming  -> author: Adhi
def stemmer(text):                          # input: teks/string
    factory = StemmerFactory()              # *seperti instansiasi library
    stemmer = factory.create_stemmer()      # create stemmer
    text = text.lower()                     # ganti huruf pada teks menjadi huruf kecil semua
    stem_text = stemmer.stem(text)          # stemming
    return stem_text                        # output: stem_text (tiap kata sudah diubah menjadi kata dasar)
# run stemmer
# teks = "Kemana uang yang kamu temukan di jalanan tadi?"
# stem = stemmer(teks)
# print(stem)
# end stemming

########################################################################################################################
# question_processing -> author: Wilis, Giffaro
def question_processor(question):           # input: pertanyaan/string
    verba = ""
    tag_search = ""

    # kata tanya: sementara hanya 5 kata_tanya
    kataTanya_ner = {"siapa" : 'PERSON', "mana" : 'LOCATION', "kapan" : 'DATE'}     # kata tanya dengan perkiraan jawaban ner_tag
    kataTanya_pos = {"apa" : 'NN', "berapa" : 'CD'}                                 # kata tanya dengan perkiraan jawaban pos_tag

    # ekstrak keyword
    keyword = stemmer(question)                                 # hasil stemming disimpan sebagai keyword

    apa = False  # kata tanya -> bukan 'apa'

    # ekstrak tag_search untuk diproses pada answer_processing
    text = nltk.word_tokenize(keyword)                          # tokenisasi keyword
    for word in text:                                           # looping tiap kata pada keyword
        if word in kataTanya_ner:                               # jika: keyword mengandung kata tanya berjawaban ner_tag
            tag_search = {'NER' : kataTanya_ner[word]}          # maka: tag_search disimpan dengan format {'NER' : ner_tag}, dimana ner_tag didapat dari pasangan kata tanya
        elif word in kataTanya_pos:                             # jika: keyword mengandung kata tanya berjawaban pos_tag
            if word == "berapa" and 'ke' in text:               # jika: kata tanya -> 'berapa' dan terdapar kata 'ke' pada pertanyaan
                tag_search = {'POS' : 'OD'}                     # maka: tag_search disimpan dengan format {'POS' : 'OD'}, dimana tag 'OD' menyatakan urutan
            else: tag_search = {'POS' : kataTanya_pos[word]}    # selain dari itu, maka: tag_search disimpan dengan format {'POS' : ner_tag}, dimana pos_tag didapat dari pasangan kata tanya
            if tag_search['POS'] == "NN": apa = True            # kata tanya -> 'apa'

    # ekstrak kata kerja dari pertanyaan,, hanya jika: kata tanya -> 'apa'
    if apa:                                         # jika: kata tanya -> 'apa'
        q = pos_tagger(question)                    # melakukan pos_tagging pada pertanyaan
        for words in q:                             # looping kalimat pertanyaan
            for word in words:                      # looping tiap pasangan kata dan tag
                if word[1] == 'VB':                 # jika: tag dari kata merupakan 'VB'
                    verba = word[0]                 # maka: kata dengan tag tersebut disimpan sebagai verba

    # hasil
    return keyword, tag_search, verba           # output: keyword, tag_search, verba

########################################################################################################################
# passage_retieval -> author: Wilis, Brillian, Giffaro
def passage_retieval(text, keyword):    # input: text/string, keyword/string
    keyword = keyword.split(' ')        # pisah keyword menjadi tiap kata
    text = text.split(".")              # pisah teks menjadi tiap kalimat

    # format dokumen
    doc = []; doc_id = 0
    for sentence in text:               # looping tiap kalimat pada keseluruhan teks
        if len(sentence) != 0:          # jika: bukan kalimat kosong,
            dict = {'id': doc_id, 'bobot': 0, 'passage': sentence}  #format
            doc.append(dict)            # simpan format kalimat sebagai dokumen (1 *kalimat -> 1 *dokumen)
            doc_id += 1                 # increment id dokumen

    # pembobotan dokumen
    bobot_max = 0; doc_id = []
    for sentence in doc:                                    # looping tiap dokumen (tiap kalimat),, kalimat -> dokumen)
        sentence['passage'] = stemmer(sentence['passage'])  # stemming dokumen
        token = nltk.word_tokenize(sentence['passage'])     # tokenisasi dokumen menjadi token
        for any in token:                                   # looping tiap token
            if any in keyword:                              # jika: token sama dengan keyword,
                sentence['bobot'] += 1                      # maka: bobot dokumen ditambah
        if bobot_max < sentence['bobot']:                   # jika: bobot dokumen lebih besar dari bobot terbesar,
            bobot_max = sentence['bobot']                   # maka: simpan bobot dokumen sebagai bobot terbesar

    # ambil doc_id dengan bobot terbesar
    for sentence in doc:                        # looping tiap dokumen
        if sentence['bobot'] == bobot_max:      # jika: bobotnya sama dengan bobot terbesar,
            doc_id.append(sentence['id'])       # maka: simpan id dari dokumen tersebut

    # ekstrak relevant_passage
    relevant_passage = []
    for id in doc_id:                           # looping tiap id dokumen dengan bobot terbesar
        relevant_passage.append(text[id])       # simpan teks dengan id tersebut sebagai dokumen yang relevan

    # hasil
    return relevant_passage                     #output: relevant_passage
# run passage_retieval
# text = """Ani pergi ke pasar untuk membeli sayur. Joni pergi ke pasar untuk membeli buah. Rani pergi ke toko elektronik untuk membeli kulkas."""
# keyword = "pasar"
# relevant_passage = passage_retieval(text, keyword)
# print(relevant_passage)
# end passage_retrieval

########################################################################################################################
# answer_processor -> author: Wilis
def answer_processor(passage, tag_search, verba):   # input: passage, tag_search, verba
    answer = ""

    # pemisahan proses jawaban menggunakan ner_tagger dengan pos_tagger
    for tag in tag_search:                          # looping tag yang akan dicari: ner_tag/pos_tag
        # penggunaan ner_tagger
        if tag == "NER":                            # jika: tag -> ner_tag
            # sementara hanya ekstrak jawaban dari 1(satu) passage yang cocok
            passage = ner_tagger(passage[0])        # passage diberi ner_tag

            # ekstrak jawaban dari passage
            for words in passage:                   # looping tiap kata dari passage
                if words[1] == tag_search[tag]:     # jika: tag kata sesuai dengan ner_tag yang dicari:
                    if answer != "":                # jika: jawaban tidak kosong
                        answer += " dan "           # maka: ditambahkan kata "dan"
                    answer += words[0]              # maka: kata dengan ner_tag tersebut disimpan sebagai jawaban
                    if tag_search[tag] != "PERSON": # jika: ner_tag yang dicari bukan person, maka looping dihentikan
                        break                       # looping dihentikan

            #format tanggal
            if tag_search[tag] == "DATE":                                          # jika: ner_tag -> "DATE"
                if re.search("(\d{1,}\-[A-Za-z]{3,}\-\d{4})", answer) != None:     # jika: format tanggal -> dd-month-yyyy
                    answer = re.sub("-", " ", answer)                              # maka: tanda "-" diganti spasi

        # penggunaan pos_tagger
        elif tag == "POS":
            # sementara hanya ekstrak jawaban dari 1(satu) passage yang cocok
            passage = pos_tagger(passage[0])   # passage diberi pos_tag

            # untuk kata tanya -> 'apa'
            if verba != '':                             # verba hanya ada jika kata tanya -> 'apa'
                # ekstrak jawaban dari passage
                for words in passage:                   # looping tiap kata dari passage
                    for i in range(len(words)):         # ideks kata
                        if stemmer(words[i][0]) == stemmer(verba) and words[i + 1][1][0:2] == tag_search[tag]:    # jika: verba dari pertanyaan diikuti langsung oleh kata dengan tag 'NN'(tag diawali 'NN', jadi tag 'NNP' juga termasuk) **misal: (membeli/VB, buku/NN)
                            answer = words[i + 1][0]    # maka: kata dengan tag 'NN' tersebut disimpan sebagai jawaban
                            break                       # looping dihentikan

            #untuk kata tanya -> 'berapa'
            else:
                if tag_search[tag] == 'CD':                             # jika: menanyakan umur **misal -> berapa usia/umur...
                    for words in passage:                               # looping tiap pasangan kata dan tag
                        for i in range(len(words)):                     # indeks looping
                            if words[i][1] == tag_search[tag] and words[i + 1][0] == 'tahun':   # jika: terdapat kata dengan tag 'CD' diikuti dengan kata 'tahun'
                                answer += words[i][0] + ' tahun'        # maka:
                                break                                   # looping dihentikan
                else:                                                   # jika: menanyakan urutan **misal -> ...ke berapa...
                    for words in passage:                               # looping semua pasangan kata dan tag
                        for i in range(len(words)):                     # indeks looping
                            if words[i][1] == tag_search[tag]:          # jika: terdapat kata dengan tag sama seperti tag yang dicari, **tag seharusnya -> 'OD'
                                answer += words[i][0]                   # maka: kata tersebut disimpan sebagai jawaban
                                break                                   # looping dihentikan

    # hasil
    return answer               # output: answer