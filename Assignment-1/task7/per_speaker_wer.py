#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
import sys


# In[13]:


#wer_path = './exp/tri1/decode_test/scoring_kaldi/wer_details/per_spk'
wer_path = sys.argv[1]


# In[76]:


data = pd.read_csv(wer_path,delim_whitespace=True)
data


# In[77]:


result = pd.merge(data, data,how="inner",left_on='SPEAKER',right_on='SPEAKER')


# In[78]:


result = result[(result['id_x']=='raw')&(result['id_y']=='sys')]
#result[(result['SPEAKER']=='SUM')]
result = result[:-1]


# In[91]:


for row in result.itertuples():
    print(row[1]," ",row[-2]," [ ",int(row[5])," / ",row[4],", ",int(row[6])," ins, ",int(row[7])," del, ",int(row[8])," sub ]",sep="")

