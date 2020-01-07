import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from sklearn.metrics import roc
# from sklearn.model_selection import traintestsplit
# from sklearn.preprocessing import 
import json
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer




def full_clean(raw_data_json_file):
    
    raw_data = pd.DataFrame(pd.read_json(raw_data_json_file))

    # use json lib to parse first level of json file
    raw_data = pd.io.json.json_normalize(raw_data.data)
    data=raw_data.copy()
    # creating df that contains the questions, answers and context only
    qac = data.paragraphs.apply(pd.io.json.json_normalize)
    
    #create empty dataframe with extra space
    df = pd.DataFrame(data ={ 'context':[x for x in range(150000)], 
                             'question': [x for x in range(150000)], 
                             'answers': [x for x in range(150000)], 
                             'plausible_answers': [x for x in range(150000)], 
                             'is_impossible': [x for x in range(150000)]})
    for c in df.columns:
        df[c] = 0

    k=0
    n=0
    for j in qac:
        for i in j['qas']:
            cont = str(j['context'][n])
            for m in i:
                if m['is_impossible']==True:
                    df['is_impossible'][k] = 1 
                    df['question'][k] = m['question']
                    df['plausible_answers'][k] = m['plausible_answers'][0]['text']
                    df['answers'][k] = ''
                    df['context'][k] = cont
                else:
                    df['question'][k] = m['question']
                    df['plausible_answers'][k] = ''
                    df['answers'][k] = m['answers'][0]['text']
                    df['context'][k] = cont
                k+=1

            n+=1
        n=0
        
    df = df.loc[df.context!=0]
        
    return df
        
    
    
def preprocessing(df, columns_list, lemm=True, stem=True):
    new_df = df.copy()
    
    porter = PorterStemmer()
    lemmy = WordNetLemmatizer()
    
    
    for col in columns_list:
        try:
            new_df.col.apply(nltk.word_tokenize)
            new_df.col.apply(lemmy.lemmatize)
    