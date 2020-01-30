

import sys
import pandas as pd
import glob
import numpy as np


homedir = './PATENT_DIR/'
print('')
print('CREATE_RECOMMENDER_DATA_FILE.py--------------------')

#find the target file and get target keywords and counts
tar_file = glob.glob(homedir+"target_*.csv")
print('Target_file: ',tar_file[0])
tar_df = pd.read_csv(tar_file[0])
print('Target Kw Freq: \n',tar_df)
target_kw = tar_df['KEYWORD'].values.tolist()
#print(target_kw)
target_cnt = tar_df['COUNT'].values.tolist()
#print(target_cnt)

stem = tar_file[0].strip('.csv')
stem = stem.strip(homedir)
target_pat = stem.strip('target_')

target_df_data = {'KEYWORD':target_kw, target_pat:target_cnt}
target_df = pd.DataFrame(data=target_df_data)


filelist = glob.glob(homedir+"*.csv")

for i in range(len(filelist)):
    if 'output' not in filelist[i] and 'target' not in filelist[i]:
        df = pd.read_csv(filelist[i])
        stem = filelist[i].strip('.csv')
        stem = stem.strip(homedir)
#        kwlist = ['Patent Number']; cntlist = [stem.strip(homedir)]
        kwlist = []; cntlist = []
#        print(filelist[i])
#        print(df)
        for kw in target_kw:
            if kw in df['KEYWORD'].values:
                for idx in df['KEYWORD'].index:
                    if kw == df['KEYWORD'][idx]:
                        cnt = df['COUNT'][idx]
                        kwlist.append(kw)
                        cntlist.append(cnt)
            else:
                kwlist.append(kw)
                cntlist.append(0)
                
        d = {'COUNT':cntlist}
        new_df = pd.DataFrame(data=d)
        target_df[stem] = new_df['COUNT'].values
target_df.T.to_csv(r'./export_patents.csv')
print('Keyword freq matrix of all searched patents (First patent is target): \n')
print(target_df.T, sep=',')
