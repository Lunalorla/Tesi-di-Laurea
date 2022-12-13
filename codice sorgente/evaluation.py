import numpy as np
import scipy as sc
from sklearn.metrics.pairwise import cosine_similarity
import os
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import spearmanr

#FUNZIONE similarità ita
path = 'File_elaborati/Ita/Token_Nomi/Vecs_Token/vecs_token_%s.npy'

tot_scores = []
wordn_senses = []
wiki_senses = []
fr = []

# #scorri tra i file per la classe semantica per cls/token
fp = open('file_complete/Nomi_Complete.txt', 'r', encoding='utf-8')
for line in fp:
  line = line.strip().split('\t')
  word = line[0]
  f = path%word
  if os.path.isfile(f):#controllo se il file esiste
    if line[1] == '-1':
      continue
    wordn_senses.append(line[1])#numero di sensi di wordnet
    if line[2] == '-1':
      del wordn_senses[-1]
      continue
    wiki_senses.append(line[2])#numero di sensi di wiktionary
    fr.append(line[3]) #frquenza assoluta
  
    M = np.load(f)

    cos_sim = cosine_similarity(M,M)

    scores = []

    for i in range(len(cos_sim)):
      for j in range(len(cos_sim)):
        if i > j:
          scores.append(cos_sim[i,j])


    score = sum(scores)/len(scores)
    tot_scores.append(score)


# confronto tra tutti gli score di similarità e i sensi di wordnet  e wiktionary
print('\nClasse Semantica Verbi\tVecs_Token :\n\nSpearman tra score di similarità e numero di sensi di wiktionary:  ', spearmanr(tot_scores,wiki_senses))
print('Spearman tra score di similarità e numero di sensi di wordnet:  ',spearmanr(tot_scores,wordn_senses))

print('Spearman tra e numero di sensi di wiktionary e numero di sensi di wordnet:  ',spearmanr(wiki_senses,wordn_senses))

print('Spearman tra numero di sensi di wiktionary e numero di frequenze assolute:  ',spearmanr(wiki_senses,fr))
print('Spearman tra numero di sensi di wordnet e numero di frequenze assolute:  ',spearmanr(wordn_senses,fr))
print('Spearman tra score di similarità e numero di frequenze assolute:  ',spearmanr(tot_scores,fr))

#FUNZIONE intersezione ita

path = 'File_elaborati/Ita/Token_Verbi/Token_Score/%s_TokenScore.txt'

int_scores = []
wordn_senses = []
wiki_senses = []

fp = open('file_complete/Verbi_Complete.txt', 'r', encoding='utf-8')
for line in fp:
  line = line.strip().split('\t')
  word = line[0]
  f = path%word
  if os.path.isfile(f):
    if line[1] == '-1':
      continue
    wordn_senses.append(line[1])
    if line[2] == '-1':
      del wordn_senses[-1]
      continue
    wiki_senses.append(line[2])
  
    tk = open(f, 'r', encoding='utf-8')
    set_list = []
    word_list = []

    for line in tk:
      line = line.strip().split('\t')
      for l in line:
        l = l.split(' ')[0]
        word_list.append(l)
      set_list.append(set(word_list))    
      word_list.clear()

    scores = []

    for i in range(len(set_list)):
      for j in range(len(set_list)):
        if i < j:
          scores.append(len(set.intersection(set_list[i],set_list[j])))

    score = sum(scores)/len(scores)
    int_scores.append(score)



print('\nSpearman tra score di intersezione e numero di sensi di wiktionary:  ',spearmanr(int_scores,wiki_senses))
print('Spearman tra score di intersezione e numero di sensi di wordnet:  ',spearmanr(int_scores,wordn_senses))

# A PARTE dopo le due funzioni

print('Spearman tra score di intersezione e score di similarità:  ',spearmanr(int_scores,tot_scores))


#creazione grafico sui vecs_token

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.bar(wordn_senses, tot_scores, label = 'wordnsenses', color= 'orange')
ax.plot(wordn_senses, tot_scores, label = 'Token_Scores', color= 'blue')
fig.suptitle('Vecs_Token Nomi')
ax.legend()

plt.show()

