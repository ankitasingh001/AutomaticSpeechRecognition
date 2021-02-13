#!/usr/bin/env python
# coding: utf-8

# In[45]:


import sys
import os
import subprocess


# In[41]:


ctm_path = '../exp/tri1/ctm'
output_path = 'outputaudio'
f =open(ctm_path)
utt_dict =[]
for lines in f.readlines():
    
    #print(lines)
    utt = lines.split()
    utterance = utt[0]
    word =utt[-1]
    start_time = utt[-3]
    duration = utt[-2]
    #print(word,start_time,end_time)
    utt_dict.append([word,start_time,duration,utterance])


# In[23]:


phrase =[]
#phrase = sys.argv[1].split()
for i in range(1,len(sys.argv)):
    phrase.append(sys.argv[i])
#print(phrase)

#print(len(phrase))

# In[33]:


'''
temporary declaration
'''
#phrase = ['nami', 'pendo', 'pondo']


# In[48]:


len_phrase = len(phrase)
counter =0
if not os.path.exists('outputaudio'):
    os.makedirs('outputaudio')
for i in range(0,len(utt_dict)-len_phrase):
    match = True
    dur =0.0
    for j in range(0,len_phrase):
        #print(utt_dict[i+j][0],phrase[j])
        if(utt_dict[i+j][0]!=phrase[j]):
            match = False
            break
        dur = dur+ float(utt_dict[i+j][2])
    if(match):
        counter+=1
        countstr = str(counter)
        countstr = countstr.rjust(2, '0')
        left = utt_dict[i][1]
        user = utt_dict[i][3][:15]
        filename = utt_dict[i][3]
        #print(user,left,dur)
        bashCommand = 'sox ../corpus/data/wav/{}/{}.wav outputaudio/word{}.wav trim {} {}'.format(user,filename,countstr,left,dur)
        #print(bashCommand)
        output = subprocess.check_output(['bash','-c', bashCommand])
        

