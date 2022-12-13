import json
from nltk.corpus import wordnet as wn

#funzione che costruisce un dizionario che ha come chiavi le parole polisemiche prelevate da wordnet e come valori il loro numero di sensi
#per controllare che una parola sia polisemica e quindi inserirla all'interno del dizionario, viene fatto un controllo sul numero di sensi,
#se maggiore di 1 viene inserita altrimenti scartata, infine il dizionario viene ordinato sui sensi, in maniera decrescente
def searchingPolysemyWordnet(pos): 

    cont = 0

    wordnet_dict = {}
    lemma_list = []
    synset_list = list(wn.all_synsets(pos)) #pos è l'equivalente della classe sintattica 'n' etc...

    for synset in synset_list:
        lemma_list.extend(synset.lemma_names(lang="ita"))
        for i in range(cont, len(lemma_list)):
            lemma = lemma_list[cont]
            if(len(wn.synsets(lemma, lang="ita")) > 1):
                sense_number = len(wn.synsets(lemma, lang="ita"))
                lemma = lemma.replace("_", " ").lower()
                wordnet_dict[lemma] = sense_number
                cont += 1
            else:
                lemma_list.remove(lemma)

    if 'gap!' in wordnet_dict:
        del wordnet_dict['gap!']
    if 'pseudogap!' in wordnet_dict:     
        del wordnet_dict['pseudogap!']
        
    wordnet_dict = dict(sorted(wordnet_dict.items(), key=lambda x: x[1], reverse=True)) #ordinamento del dizionario sui valori, in maniera decrescente
    return wordnet_dict

#funzione che stampa chiavi e valori di un dizionario su file di testo
def savingDictToFile(words_dict, filename):

    with open(filename, 'w', encoding="utf-8") as fp:
        for key, value in words_dict.items(): 
            fp.write('%s\t%s\n' % (key, value))

#funzione che stampa un dizionario innestato su file di testo
def savingNestedDictToFile(words_dict, filename):

    i = 0
    with open(filename, 'w', encoding="utf-8") as fp: 

        while i < len(words_dict):
            for value in words_dict[i].values():
                fp.write('%s\t' % (value))
            fp.write('\n')
            i += 1

#funzione che cerca parole polisemiche dal file JSON, contenente dati pre-estratti dal Wiktionary italiano 
#fa un controllo sul numero di sensi per ogni parola, se maggiore di 1 allora verrà inserita all'interno del dizionario altrimenti verrà scartata
def searchingPolysemyWiktionary(file): 

    i = 0

    wiktionary_dict = {}
    sense_word_list = []#lista creata per poter contare il numero di sensi delle parole estratte

    synset_list = [json.loads(line) for line in open(file,'r')]

    for synset in synset_list:
        limite = len(synset['senses'])
        try:
            while i < limite:
                try:
                    lemma = synset['senses'][i]['form_of'][0]['word']
                    lemma = lemma.lower()
                    sense_word_list.append(synset['senses'][i]['raw_glosses'])
                    i += 1
                    sense_number = len(sense_word_list)
                    if(sense_number > 1):
                        wiktionary_dict[lemma] = sense_number
                except KeyError: #viene gestita l'eccezione nel caso in cui la chiave form_of non sia presente, prendendo il lemma dalla chiave word
                    lemma = synset['word']
                    lemma = lemma.lower()
                    sense_word_list.append(synset['senses'][i]['raw_glosses'])
                    i += 1
                    sense_number = len(sense_word_list)
                    if(sense_number > 1):
                        wiktionary_dict[lemma] = sense_number
        except KeyError: #viene gestita l'eccezione nel caso in cui la chiave raw_glosses non sia presente, scartando la parola
            i = 0
            sense_word_list.clear()
        i = 0
        sense_word_list.clear()

    wiktionary_dict = dict(sorted(wiktionary_dict.items(), key=lambda x: x[1], reverse=True)) #ordinamento del dizionario sui valori, in maniera decrescente
    return wiktionary_dict

#funzione che conta il numero di frasi presenti nel corpus
def countingPhrases(file):

    phrases_count = 0

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if line == "\n":
                phrases_count += 1

    phrases_count -= 1
    return phrases_count

#funzione che si occupa della creazione di un dizionario innestato completo di numero di sensi per Worndet e Wiktionary, frequenza assoluta e frequenza relativa.
def creatingDict(dictCorpus, dictWordnet, dictWiktionary, filename):

    phrases_count = countingPhrases(filename)
    i= 0
    words_dict = {}

    for key in dictCorpus.keys():
        f_assoluta = dictCorpus[key]
        f_relativa = f_assoluta/phrases_count
        if key in dictWordnet and key in dictWiktionary:
            words_dict[i] = {'nome_parola': key, 'n_sensi_wordnet' : dictWordnet[key], 'n_sensi_wiktionary': dictWiktionary[key], 'freq_assoluta': f_assoluta, 'freq_relativa': f_relativa}
            i += 1
        elif key not in dictWordnet and key in dictWiktionary:
            words_dict[i] = {'nome_parola': key, 'n_sensi_wordnet' : -1, 'n_sensi_wiktionary': dictWiktionary[key], 'freq_assoluta': f_assoluta, 'freq_relativa': f_relativa}
            i += 1
        elif key in dictWordnet and key not in dictWiktionary:
            words_dict[i] = {'nome_parola': key, 'n_sensi_wordnet' : dictWordnet[key], 'n_sensi_wiktionary': -1, 'freq_assoluta': f_assoluta, 'freq_relativa': f_relativa}
            i += 1

    return(words_dict)