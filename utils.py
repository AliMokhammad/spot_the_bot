import os
import re
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import (normalize_alef_maksura_ar,normalize_alef_ar,normalize_teh_marbuta_ar)
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.ner import NERecognizer

global mle
mle = MLEDisambiguator.pretrained()

## define  label_dict ##
ner = NERecognizer.pretrained()
# ner.labels() == ['B-LOC', 'B-ORG', 'B-PERS', 'B-MISC', 'I-LOC', 'I-ORG', 'I-PERS', 'I-MISC', 'O']

ner_labels = ner.labels()
ner_default_value = ner_labels[-1]

print(ner_default_value)
label_dict = {'NUM':'0','PRON':'1'}
label_dict_idx = 0
while (label_dict_idx < len(ner_labels)):
  if(ner_labels[label_dict_idx] != ner_default_value):
    label_dict[ner_labels[label_dict_idx]] =  str(label_dict_idx + 2) 
  label_dict_idx += 1

print(label_dict)

def check_dir (d):
    if not os.path.exists(d):
        os.makedirs(d)
### prepare text using camel tool ###
def clean_text_with_camel_utils(text):
    text = dediac_ar(text)
    text = normalize_alef_maksura_ar(text)
    text = normalize_alef_ar(text)
    text = normalize_teh_marbuta_ar(text)
    return text
### delete non-arabic chars and non-numbers  ###
def clean_arabic_text(text):
    cleaned_text = re.sub(r'[^\u0600-\u06FF\d\u064B-\u0652\s]', '', text)
    return cleaned_text.strip()


### replace digits with 0 ###
def clean_text_digits(text):
    text = re.sub(r'\d+', label_dict['NUM'] , text)
    return text
    
### read clean csv dataset file function ###
def clean_dataset(data_list, should_normalize=True):
  new_data_list = []
  for line in data_list:
    line = clean_arabic_text(line)
    line = clean_text_digits(line)
    if(should_normalize): line = clean_text_with_camel_utils(line)
    if(len(line)): new_data_list.append(line)
  return new_data_list

def replace_text_ner(text_tokens):
  labels = ner.predict_sentence(text_tokens)
  #print(labels,"labels")
  #print(text_tokens,"text_tokens")
  token_idx=0
  for label in labels:
    if(label != ner_default_value):
      text_tokens[token_idx] = label_dict[label]
    token_idx+=1
    #print(text_tokens)
  return " ".join(text_tokens),text_tokens


### data_frames_text disambiguation function ###
def disambiguate_text_tokens (text_tokens):
  disambig = mle.disambiguate(text_tokens)
  diacritized = []
  pos_tags = []
  lemmas = []
  for d in disambig:
    if len(d.analyses) == 0:
      diacritized.append(None)
      pos_tags.append(None)
      lemmas.append(None)
      continue
    analysis = d.analyses[0].analysis
    # print(analysis)
    diacritized.append(analysis['diac'])
    pos_tags.append(analysis['pos'])
    # lemmas.append(analysis['lex'])
    lemmas.append(dediac_ar(analysis['lex']))
    # lemmas.append(analysis['root'].replace(".", ""))
  return pos_tags, lemmas, diacritized

########
# tags_classes = ['adv_interrog', 'digit', 'part_verb', 'part_voc', 'adj', 'interj', 'part_focus', 'adv_rel', 'pron', 'prep', 'verb_pseudo', 'adv', 'foreign', 'noun_quant', 'part', 'conj_sub', 'punc', 'pron_dem', 'part_interrog', 'verb', 'pron_rel', 'part_det', 'abbrev', 'noun', 'part_neg', 'conj', 'noun_prop']
def add_word_to_class_dict(d, k, w):
  if k in d: d[k].append(w)
  else: d[k] = [w]


######
def delete_punc(text_tokens,pos_tags):
  token_idx=0
  d = {}
  for tag in pos_tags:
    add_word_to_class_dict(d, tag, text_tokens[token_idx])
    if(tag == 'punc'):
      # text_tokens[token_idx] = None
      text_tokens[token_idx] = ""
    token_idx+=1
  # print(text_tokens)
  # text_tokens = list(filter(lambda el: not not el, text_tokens))
  # print(d)
  return " ".join(text_tokens),text_tokens


### change all pronoun to 1 ###
def replace_pronoun_to_1(text_tokens,pos_tags):
  token_idx=0
  for tag in pos_tags:
    if(tag == 'pron'):
      text_tokens[token_idx] = label_dict['PRON']
    token_idx+=1
  # print(text_tokens)
  # print("token_idx",token_idx)
  return " ".join(text_tokens),text_tokens



#######
def prepare_arabic_text(clean_data_list):
  arabic_text = clean_text_digits("\n".join(clean_data_list))
  arabic_text_tokens = simple_word_tokenize(arabic_text)
  
  arabic_text, arabic_text_tokens = replace_text_ner(arabic_text_tokens)
  # print(arabic_text_tokens)

  arabic_pos_tags, arabic_lemmas, arabic_diacritized = disambiguate_text_tokens(arabic_text_tokens)
  print(arabic_lemmas[0])
 
  # arabic_text,arabic_text_tokens = delete_punc(arabic_text_tokens,arabic_pos_tags) # commented after call with Alexandra # we should take lemmas
  arabic_text,arabic_lemmas = delete_punc(arabic_lemmas,arabic_pos_tags)

  # arabic_text, arabic_text_tokens = replace_pronoun_to_1(arabic_text_tokens,arabic_pos_tags)
  arabic_text, arabic_lemmas = replace_pronoun_to_1(arabic_lemmas,arabic_pos_tags)
  # arabic_text_tokens = list(filter(lambda t: len(t.strip()) != 0, arabic_text_tokens))  # commented after call with Alexandra # we should take lemmas
  arabic_lemmas = list(filter(lambda t: len(t.strip()) != 0, arabic_lemmas))

  # arabic_text = "\n".join(arabic_text_tokens)  # commented after call with Alexandra # we should take lemmas
  arabic_text = "\n".join(arabic_lemmas)

  # return arabic_text, arabic_text_tokens 
  return arabic_text, arabic_lemmas # commented after call with Alexandra # we should take lemmas

