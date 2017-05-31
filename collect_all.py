# -*- coding: utf-8 -*-
"""
Created on Sun May 28 09:51:46 2017

@author: Quantum Liu
"""
from pornspider import *
try:
    with open('pornhub.pkl','rb')as f:
        pornhub=pickle.load(f)
except:
    pornhub=site()
st=time.time()
n=0
pornhub.init_category(name_list=pornhub.category_name_list)
for name in pornhub.category_name_list:
    print('Collecting category: '+name)
    pornhub.iterate_videos(category_name=name,num_page=5,start_page=1,iterate_all=True)
    n+=len(pornhub.category_dict[name].videos)
print('Number of videos :',n,'Average time costing : '+str(n/(time.time()-st))+'page/s')
with open('pornhub.pkl','wb')as f:
    pickle.dump(pornhub,f)
