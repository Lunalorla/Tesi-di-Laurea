import random
import gzip
from transformers import AutoTokenizer
from transformers import AutoModel
from transformers import pipeline
import torch
import numpy as np
import pickle

def get_embedding(sentence_l,target,sentence_r,strategy='mean'):
    model.eval()
    with torch.no_grad():
      tokens = []
      tokens_l = tokenizer.tokenize(sentence_l)
      tokens = tokens + tokens_l

      start = len(tokens)

      tokens_target = tokenizer.tokenize(target)
      tokens = tokens + tokens_target

      end = len(tokens)

      tokens_r = tokenizer.tokenize(sentence_r)
      tokens = tokens + tokens_r

      if len(tokens) > 512:
         return None

      input_ids = tokenizer.convert_tokens_to_ids(tokens)

      input_mask = torch.tensor([[1] * len(input_ids)])

      input_ids = torch.tensor([input_ids])

      outputs = model(input_ids.to('cuda'),attention_mask=input_mask.to('cuda'))
      hidden_states = outputs['hidden_states'][-1].cpu().detach().numpy()

      if strategy == 'mean':
        return np.mean(hidden_states[-1][start:end],axis=0)
      else:
        return hidden_states[-1][0]

#estrazione parole target e salvataggio in lista, in base alla classe semantica
def target_extraction(filename, semantic_class):

  targets = []

  with open(filename, 'r', encoding = "utf-8") as f:
    f.readline()
    for line in f:
        line = line.strip().split("\t")[1].split("_")
        word = line[0]
        sem_class = line[1]
        if sem_class == semantic_class:
          targets.append(word)
  return targets

#funzione che crea un dizionario dove ogni parola target avrà tot frasi in cui compare
def create_sentences(filename, targets):

  sentences = {} #creazione dizionario vuoto

  with gzip.open(filename, 'rb') as f:

      for target_word in targets:

          sentences[target_word] = [] #creo la chiave nel dizionario in base alla parola osservata
          temp_list = []

          for line in f:

              try:
                file_content = line.strip().decode('UTF-8').split("\t") #decodifico e splitto la stringa escludendo la parola target all'inizio della riga
              except UnicodeDecodeError:
                file_content = line.strip().decode('ISO-8859-1').split("\t")
              
              #ricavo i componenti necessari
              first_word = file_content[0] #parola ad inizio riga
              start = int(file_content[1]) #inizio della occorrenza target
              end = int(file_content[2]) #fine dell'occorrenza target
              file_content = file_content[3] #contesto

              #controllo se la parola ad inizio riga è uguale alla parola target che stiamo cercando
              if first_word == target_word:

                  #estraggo i contesti
                  target_occ = file_content[start:end]
                  left_context = file_content[:start]
                  right_context = file_content[end:]

                  sentence = [left_context,target_occ,right_context]#costruzione esempio con contesto destro, occorrenza della parola target e contesto destro
                  temp_list.append(sentence)

          f.seek(0)
          
          lun = len(temp_list)
          number_range=range(0,lun)

          if len(temp_list) > 100:
              number_list = random.sample(number_range,100)
              l = 0
              while l < 100:
                  sentence = temp_list[number_list[l]]
                  sentences[target_word] += [sentence] #aggiunta della parola target al dizionario con contesti e occorrenze
                  l += 1
          else:
              for el in temp_list:
                  sentence = el
                  sentences[target_word] += [sentence]
  return sentences

#CREAZIONE MODELLO

model_checkpoint = 'dbmdz/bert-base-italian-xxl-uncased'
    
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

model = AutoModel.from_pretrained(model_checkpoint,output_hidden_states=True)

model.to('cuda')

nlp_fill = pipeline('fill-mask', model='dbmdz/bert-base-italian-xxl-uncased')

# targets = ['mela']
# #qui devi mettere tutte le parole target

# sentences = {'mela': [['Ho mangiato delle ','mele',' rosse.']]}
# #qui devi salvare left_context, target e right_context

#ESTRAZIONE PAROLE TARGET PER CLASSE SEMANTICA
targets = target_extraction('top1000_dictionary_as_text.txt', 'NOUN') #altre classi: NOUN, ADV, ADJ

#CREAZIONE DIZIONARIO DI PAROLE TARGET CON FRASI
sentences = create_sentences('wic_it_nomi.txt.gz', targets)

#per le parole italiane che trovi nelle coppie ita-eng, prendi la lista di quelle, prendi la lista di quelle ita di base, sottrai da nuove le vecchie e poi crea sentences sulle nuove con meno roba

#CREAZIONE FILE CON MASKING E TOKEN

for i,target in enumerate(targets):
  vecs_token = []
  vecs_cls = []
  mapp = {}

  with open('File_elaborati/Token_Nomi/Token_Score/%s_TokenScore.txt'%target, 'w+', encoding = 'utf-8') as fp:

    for j, sent in enumerate(sentences[target]):
      left_context, target_occ, right_context = sent

      vec_token = get_embedding(left_context,target_occ,right_context,strategy='mean')
      if vec_token is not None:
        vecs_token.append(vec_token)
        vec_cls = get_embedding(left_context,target_occ,right_context,strategy='cls')
        vecs_cls.append(vec_cls)
        try:
          fills = nlp_fill(left_context + '[MASK]' + right_context, top_k=20)
        except RuntimeError:
          del vec_token[-1]
          del vec_cls[-1]
          continue
        mask_line = ""
        for f in fills:
          token = f['token_str']
          score = f['score']
          if len(mask_line) == 0:
              mask_line = token + ' ' + str(score)
          else:
              mask_line = mask_line + '\t' + token + ' ' + str(score)
        fp.write(f'{mask_line}\n')
            
        mapp[i] = j
  
  with open('File_elaborati/Token_Nomi/mapping_dict.txt', 'wb+') as f:
        pickle.dump(mapp,f)

  vecs_token = np.array(vecs_token)
  np.save('File_elaborati/Token_Nomi/Vecs_Token/vecs_token_%s.npy'%target,vecs_token)

  vecs_cls = np.array(vecs_cls)
  np.save('File_elaborati/Token_Nomi/Vecs_cls/vecs_cls_%s.npy'%target,vecs_cls)

# m = np.load('File_elaborati/Verbi_it/vecs_token_mela.npy') # se vuoi vedere la matrice prodotta
# print(m)