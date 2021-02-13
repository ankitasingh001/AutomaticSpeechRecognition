#!/usr/bin/env python
# coding: utf-8

# In[67]:


import pandas as pd
import os
import glob
import re
import csv
import os
from operator import add
from pathlib import Path
import indicnlp
import codecs
from collections import defaultdict
import subprocess


# In[71]:

os.chdir("../")
data_path ='./corpus/data'
corpus_path = './corpus/data/wav/'
transcriptions ='./corpus/data/transcriptions.txt'
data_info_path = './corpus/data/data-info.txt'
utils_path = './utils/utt2spk_to_spk2utt.pl'


# In[15]:


data = pd.read_csv(data_info_path, sep=" ", header=None)


# In[38]:


'''
Transpose data from datainfo.txt and get columns for each of train,test and truetest
'''
df = data.transpose()
new_header = df.iloc[0] 
df = df[1:] 
df.columns = new_header


# In[97]:


for column in df:
    d_path = data_path +'/'+column
    if not os.path.exists(d_path):
        os.makedirs(d_path)
    speakers = df[column].dropna()
    wavscp_path = d_path+'/'+'wav.scp'
    text_path = d_path +'/'+'text'
    utt2spk_path = d_path +'/'+'utt2spk'
    spk2utt_path = d_path +'/'+'spk2utt'
    f1 = open(wavscp_path, "w+")
    f2 = open(utt2spk_path,"w+")
    f3 = open(text_path,"w+")
    for i in range(1,speakers.size+1):
        speaker = speakers.get(i)
        speaker_path = d_path+'/'+ speaker
        speaker_data_path = corpus_path+ speaker
        for file in Path(speaker_data_path).glob('**/*.wav'):
            path =str(file).split(".")[0]
            utterance_id =path.split("/")[-1]
#             print(utterance_id)
#             print(speaker)
            f1.write(utterance_id+" "+str(file)+"\n")
            f2.write(utterance_id+" "+speaker+"\n")
            f4 = open(transcriptions,"r")
            for line in f4:
                if (line.split('\t')[0] == utterance_id):
                    f3.write(line)
        
    bashCommand = "sort "+utt2spk_path+" -o "+utt2spk_path
    output = subprocess.check_output(['bash','-c', bashCommand])
    bashCommand = "sort "+wavscp_path+" -o "+wavscp_path
    output = subprocess.check_output(['bash','-c', bashCommand])
    bashCommand = "sort "+text_path+" -o "+text_path
    output = subprocess.check_output(['bash','-c', bashCommand])
    bashCommand =  "./utils/utt2spk_to_spk2utt.pl " + utt2spk_path+" > "+spk2utt_path
    output = subprocess.check_output(['bash','-c', bashCommand])
    bashCommand =  "utils/fix_data_dir.sh " + d_path
    output = subprocess.check_output(['bash','-c', bashCommand])


# In[70]:




