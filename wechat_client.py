# -*- coding: utf-8 -*-
"""
Created on Mon May 29 20:42:42 2017

@author: Quantum Liu
"""

from pornspider import *
import itchat
import random
import platform
pv=int(platform.python_version()[0])
from itchat.content import TEXT
if pv>2:
    import _thread as th
else:
    import thread as th
import os
from os import system
import re
import traceback
import platform
from requests.exceptions import ConnectionError
#==============================================================================
#==============================================================================
# A log in function call it at first
#函数，需要首先调用
#==============================================================================
def login():
    if 'Windows' in platform.system():
        itchat.auto_login(enableCmdQR=1,hotReload=True)#
    else:
        itchat.auto_login(enableCmdQR=2,hotReload=True)#
    itchat.dump_login_status()#dump
#==============================================================================
# 
#==============================================================================
def send_text(text):
    #send text msgs to 'filehelper'
    #给文件助手发送文本信息
    try:
        itchat.send_msg(msg=text,toUserName='filehelper')
        return
    except (ConnectionError,NotImplementedError,KeyError):
        traceback.print_exc()
        print('\nConection error,failed to send the message!\n')
        return
    else:
        return
def send_img(filename):
    #send text imgs to 'filehelper'
    #给文件助手发送
    try:
        itchat.send_image(filename,toUserName='filehelper')
        return
    except (ConnectionError,NotImplementedError,KeyError):
        traceback.print_exc()
        print('\nConection error,failed to send the figure!\n')
        return
    else:
        return
class wechat_session():
    def __init__(self):
        login()
        print('Loged in successfully!\n')
        send_text('Loged in successfully!\n')
        try:
            with open('pornhub.pkl','rb')as f:
                self.pornhub=pickle.load(f)
        except:
            send_text('Failed loading local pickle file, initing pornhub object...\n')
            self.pornhub=site()
        self.registe()
        self.run()
    def radio(self,n=1):
        [self.show_video_detail(video_id=v.video_id,show_pic=True) for v in[self.pornhub.video_list[k] for k in(random.sample(list(self.pornhub.video_list),n))]]
        return
    def collect(self,name_list=' , '):
        try:
            name_list=name_list.split(',')
        except:
            name_list=self.pornhub.category_name_list[:1]
        send_text('Collecting categories: '+','.join(name_list))
        self.pornhub.init_category(name_list=name_list)
        for name in name_list:
            send_text('Collecting category: '+name)
            self.pornhub.iterate_videos(category_name=name,num_page=5,start_page=1,iterate_all=True)
            n+=len(pornhub.category_dict[name].videos)
        send_text('Number of videos :',n,'Average time costing : '+str(n/(time.time()-st))+'page/s')
        return
    def list_local_categories(self,root='https://www.pornhub.com'):
        local_name_list=[k for k in self.pornhub.category_name_list if self.pornhub.category_dict.get(k,False)]
        send_text('There are '+str(len(local_name_list))+' categories.\n'+','.join(local_name_list))
    def broswe_category(self,name='',num=5,start=0):
        local_name_list=[k for k in self.pornhub.category_name_list if self.pornhub.category_dict.get(k,False)]
        if name not in local_name_list:
            self.collect(name)
        start=(int(start) if start else 0)
        _end=start+num
        msg='Brosweing category '+name
        try:
            [self.show_video_abstrct(v.video_id) for v in self.pornhub.category_dict[name].videos[start:_end]]
        except KeyError:
            send_text(traceback.format_exc())
            send_text('Got key error!Please check the name.')
        finally:
            return
    def show_video_detail(self,video_id='',pic_dir='',show_pic=False):
    #显示视频信息和封面图片
    #Show infomations and the cover oicture of the video
        try:
            video=self.pornhub.video_list[video_id]
            video.update()
            if show_pic:
                headers={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
                if not pic_dir:
                    video.pic_dir='./'+(video.info['categories'][0] if video.info['categories'] else 'Sex')
                else:
                    video.pic_dir=pic_dir
                if not os.path.exists(video.pic_dir):
                    os.mkdir(video.pic_dir)
                video.pic_path=video.pic_dir+'/'+video.title+'.jpg'
                with open(video.pic_path,'wb') as f:
                    f.write(requests.get(video.cover,headers=headers).content)
                send_img(video.pic_path)
            msg='Video: ID '+video.video_id+'\nTitle: '+video.title
            for k,v in video.mp4add.items():
                msg+='\nQuaulity '+str(k)+'P: \n'+str(v)
            for k,v in video.info.items():
                msg+='\n'+str(k)+': '+str(v)
            send_text(msg)
        except:
            send_text(traceback.format_exc())
        return
    def show_video_abstrct(self,video_id=''):
    #显示视频摘要信息
    #Show abstract infomations of the video
        try:
            video=self.pornhub.video_list[video_id]
            video.update()
            msg='Video: ID '+video.video_id+'\nTitle: '+video.title+'\nQuaulitys :'
            for k,v in video.mp4add.items():
                msg+=' '+str(k)+'P;'
            for k,v in video.info.items():
                msg+='\n'+str(k)+': '+str(v)
            send_text(msg)
        except:
            send_text(traceback.format_exc())
        return
    def save(self):
        send_text('Saving pornhun object')
        try:
            with open('pornhub.pkl','wb')as f:
                pickle.dump(self.pornhub,f)
        except:
            send_text('Failed saving pickle file !')
        return
    def GetMiddleStr(self,content='',startStr='',endStr=''):
    #get the string between two specified strings
    #从指定的字符串之间截取字符串
        try:
          startIndex = content.index(startStr)
          if startIndex>=0:
            startIndex += len(startStr)
          endIndex = content.index(endStr)
          return content[startIndex:endIndex]
        except:
            return ''
    def registe(self):
        @itchat.msg_register(TEXT)
        def auto_reply(msg):
            text=msg['Text']
            cmd={'raido':[u'电台','radio','Radio'],'collect':[u'收集','collect','Collect'],'broswe category':[u'浏览类别','Broswe category','broswe category'],'broswe video':[u'浏览视频','broswe video','Broswe video'],'enumerate categorise':[u'显示本地类别','enumerate loacal categories']}
            if msg['ToUserName']=='filehelper':
                if any((c in text) for c in cmd['raido']):
                    n=int(re.findall(r"\d+\.?\d*",text)[0])
                    self.radio(n)
                if any((c in text) for c in cmd['collect']):
                    name_list=self.GetMiddleStr(text,'[',']')
                    th.start_new_thread(self.collect,(name_list,))
                if any((c in text) for c in cmd['broswe category']):
                    name=self.GetMiddleStr(text,'[',']')
                    name=(name if name else self.pornhub.category_name_list[0])
                    start=self.GetMiddleStr(text,'{','}')
                    start=(start if start else 0)
                    num=self.GetMiddleStr(text,'(',')')
                    num=(int(num) if num else 5)
                    self.broswe_category(name=name,start=start,num=num)
                if any((c in text) for c in cmd['broswe video']):
                    video_id=self.GetMiddleStr(text,'[',']')
                    try:
                        self.show_video_detail(video_id=video_id,show_pic=True)
                    except:
                        traceback.print_exc()
                if any((c in text) for c in cmd['enumerate categorise']):
                    try:
                        self.list_local_categories()
                    except:
                        send_text(traceback.format_exc())
    def run(self):
        itchat.run()
if __name__ == '__main__':
    session=wechat_session()