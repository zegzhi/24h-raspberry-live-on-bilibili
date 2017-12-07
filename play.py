#coding:utf-8
import os
import sys
import time
import random
from mutagen.mp3 import MP3
import var_set
import shutil
import _thread

path = var_set.path #引入设置路径
rtmp = var_set.rtmp #引入设置的rtmp网址
live_code = var_set.live_code   #引入设置rtmp参数

#格式化时间，暂时没啥用，以后估计也没啥用
def convert_time(n):
    s = n%60
    m = int(n/60)
    return '00:'+"%02d"%m+':'+"%02d"%s

#移动放完的视频到缓存文件夹
def remove_v(filename):
    try:
        shutil.move(path+'/downloads/'+filename,path+'/default_mp3/')
    except Exception as e:
        print(e)
    try:
        os.remove(path+'/downloads/'+filename.replace(".flv",'')+'ok.ass')
        os.remove(path+'/downloads/'+filename.replace(".flv",'')+'ok.info')
    except Exception as e:
        print(e)
        print('delete error')

while True:
    try:
        files = os.listdir(path+'/downloads')   #获取文件夹下全部文件
        files.sort()    #排序文件，按文件名（点播时间）排序
        count=0     #总共匹配到的点播文件统计
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)): #如果是mp3文件
                audio = MP3(path+'/downloads/'+f)   #获取mp3文件信息
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                if(seconds > 600):  #大于十分钟就不播放
                    print('too long,delete')
                else:
                    pic_files = os.listdir(path+'/default_pic') #获取准备的图片文件夹中的所有图片
                    pic_files.sort()    #排序数组
                    pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                    #推流
                    print('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                try:    #放完后删除mp3文件、删除字幕、删除点播信息
                    shutil.move(path+'/downloads/'+f,path+'/default_mp3/')
                    shutil.move(path+'/downloads/'+f.replace(".mp3",'')+'.ass',path+'/default_mp3/')
                    os.remove(path+'/downloads/'+f)
                    os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.ass')
                    os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.info')
                except:
                    print('delete error')
                count+=1    #点播统计加一
            if((f.find('ok.flv') != -1) and (f.find('.download') == -1) and (f.find('rendering') == -1)):   #如果是有ok标记的flv文件
                print('flv:'+f)
                #直接推流
                print('ffmpeg -re -i "'+path+"/downloads/"+f+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -i "'+path+"/downloads/"+f+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.rename(path+'/downloads/'+f,path+'/downloads/'+f.replace("ok",""))   #修改文件名，以免下次循环再次匹配
                _thread.start_new_thread(remove_v, (f.replace("ok",""),))   #异步搬走文件，以免推流卡顿
                count+=1    #点播统计加一
        if(count == 0):     #点播统计为0，说明点播的都放完了
            print('no media')
            mp3_files = os.listdir(path+'/default_mp3') #获取所有缓存文件
            mp3_files.sort()    #排序文件
            mp3_ran = random.randint(0,len(mp3_files)-1)    #随机抽一个文件
            
            if(mp3_files[mp3_ran].find('.mp3') != -1):  #如果是mp3文件
                pic_files = os.listdir(path+'/default_pic') #获取准备的图片文件夹中的所有图片
                pic_files.sort()    #排序数组
                pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                audio = MP3(path+'/default_mp3/'+mp3_files[mp3_ran])    #获取mp3文件信息
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                #推流
                if(os.path.isfile(path+'/default_mp3/'+mp3_files[mp3_ran].replace(".mp3",'')+'.ass')):
                    print('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                else:
                    print('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
            if(mp3_files[mp3_ran].find('.flv') != -1):  #如果为flv视频
                #直接推流
                print('ffmpeg -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
    except Exception as e:
        print(e)

        