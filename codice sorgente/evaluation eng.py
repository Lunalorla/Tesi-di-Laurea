import numpy as np
import scipy as sc
from sklearn.metrics.pairwise import cosine_similarity
import os
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import spearmanr

#FUNZIONE similarità eng
path1 = 'File_elaborati/Eng/Token_Verbi/Vecs_Token/vecs_token_%s.npy'
path2 = 'File_elaborati/Ita/Token_Verbi/Vecs_Token/vecs_token_%s.npy'
path3 = 'File_elaborati/Ita-Eng/Token_Verbi/Vecs_Token/vecs_token_%s.npy'

tot_scores = []
wordn_senses = []
wiki_senses = []
fr = []

# #scorri tra i file per la classe semantica per cls/token
fp = open('verb.txt', 'r', encoding='utf-8')
for line in fp:
  line = line.strip().split('\t')
  ita_word = line[0]
  eng_word = line[1].replace('_', ' ')
  f1 = path1%eng_word
  f2 = path2%ita_word
  f3 = path3%ita_word
  if os.path.isfile(f1) and os.path.isfile(f2):#controllo se il file esiste
    if line[3] == '-1':
      continue
    wordn_senses.append(line[3])#intersezione dei sensi della parola in italiano e in inglese di wordnet
    fr.append(line[4]) #frequenza assoluta
  
    M1 = np.load(f1)
    M2 = np.load(f2)

    try:
      cos_sim = cosine_similarity(M1,M2)
    except ValueError:
      del wordn_senses[-1]
      del fr[-1]
      continue

    scores = []

    for i in range(len(cos_sim)):
      for j in range(len(cos_sim)):
        if i > j:
          scores.append(cos_sim[i,j])


    score = sum(scores)/len(scores)
    tot_scores.append(score)
  elif os.path.isfile(f1) and os.path.isfile(f3):
    if line[3] == '-1':
      continue
    wordn_senses.append(line[3])#numero di sensi di wordnet
    fr.append(line[4]) #frquenza assoluta
  
    M1 = np.load(f1)
    M2 = np.load(f3)

    try:
      cos_sim = cosine_similarity(M1,M2)
    except ValueError:
      del wordn_senses[-1]
      del fr[-1]
      continue

    scores = []

    for i in range(len(cos_sim)):
      for j in range(len(cos_sim)):
        if i > j:
          try:
            scores.append(cos_sim[i,j])
          except IndexError:
            pass

    score = sum(scores)/len(scores)
    tot_scores.append(score)


# confronto tra tutti gli score di similarità e i sensi di wordnet  e wiktionary
# per il numero di sensi, li prendi dai file creati da te, in base alla parola target

print('Classe Semantica Verbi\tVecs_cls :\n\nSpearman tra score di similarità e numero di sensi di wordnet:  ',spearmanr(tot_scores,wordn_senses))

print('Spearman tra numero di sensi di wordnet e numero di frequenze assolute:  ',spearmanr(wordn_senses,fr))

print('Spearman tra score di similarità e numero di frequenze assolute:  ',spearmanr(tot_scores,fr))


#creazione grafico sui vecs_token

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.bar(wordn_senses, tot_scores, label = 'wordnsenses', color= 'orange')
ax.plot(wordn_senses, tot_scores, label = 'Token_Scores', color= 'blue')
fig.suptitle('Vecs_Token Nomi')
ax.legend()

plt.show()