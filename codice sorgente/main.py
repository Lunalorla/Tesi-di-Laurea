from wordsSearch import *
from build_contexts import *

#Costruzione delle liste di tuple contenenti la coppia (parola polisemica,numero di sensi)
nomi_wordnet = searchingPolysemyWordnet('n')
verbi_wordnet = searchingPolysemyWordnet('v')
avverbi_wordnet = searchingPolysemyWordnet('r')
aggettivi_wordnet = searchingPolysemyWordnet('a')

nomi_wiktionary = searchingPolysemyWiktionary('File JSON/kaikki.org-dictionary-Italian-by-pos-noun.json')
verbi_wiktionary = searchingPolysemyWiktionary('File JSON/kaikki.org-dictionary-Italian-by-pos-verb.json')
avverbi_wiktionary = searchingPolysemyWiktionary('File JSON/kaikki.org-dictionary-Italian-by-pos-adv.json')
aggettivi_wiktionary = searchingPolysemyWiktionary('File JSON/kaikki.org-dictionary-Italian-by-pos-adj.json')

#Salvataggio su file di testo delle liste di tuple create
savingDictToFile(nomi_wordnet, 'File di testo/Wordnet_Nomi.txt')
savingDictToFile(verbi_wordnet, 'File di testo/Wordnet_Verbi.txt')
savingDictToFile(avverbi_wordnet, 'File di testo/Wordnet_Avverbi.txt')
savingDictToFile(aggettivi_wordnet, 'File di testo/Wordnet_Aggettivi.txt')

savingDictToFile(nomi_wiktionary, 'File di testo/Wiktionary_Nomi.txt')
savingDictToFile(verbi_wiktionary, 'File di testo/Wiktionary_Verbi.txt')
savingDictToFile(avverbi_wiktionary, 'File di testo/Wiktionary_Avverbi.txt')
savingDictToFile(aggettivi_wiktionary, 'File di testo/Wiktionary_Aggettivi.txt')

#creazione dei dizionari sulla base dei file di Wordnet e Wiktionary

build()

nomi = nomi.word_dict
verbi = verbi.word_dict
avverbi = avverbi.word_dict
aggettivi = aggettivi.word_dict

#costruzione dei dizionari completi utilizzando i dizionari precedentemente creati

nomidict = creatingDict(nomi, nomi_wordnet, nomi_wiktionary, "File d'uso/ITWAC.txt")
verbidict = creatingDict(verbi, verbi_wordnet, verbi_wiktionary, "File d'uso/ITWAC.txt")
avverbidict = creatingDict(avverbi, avverbi_wordnet, avverbi_wiktionary, "File d'uso/ITWAC.txt")
aggettividict = creatingDict(aggettivi, aggettivi_wordnet, aggettivi_wiktionary, "File d'uso/ITWAC.txt")

#Salvataggio su file di testo dei dizionari appena creati

savingNestedDictToFile(nomidict, "Nomi_Complete.txt")
savingNestedDictToFile(verbidict, "Verbi_Complete.txt")
savingNestedDictToFile(avverbidict, "Avverbi_Complete.txt")
savingNestedDictToFile(aggettividict, "Aggettivi_Complete.txt")
