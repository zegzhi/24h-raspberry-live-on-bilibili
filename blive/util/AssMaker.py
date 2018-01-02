#coding:utf-8
import os
import time
import re
import shutil
import json

class AssMaker:
    def __init__(self):
        self.ass_head = '''[Script Info]
Title: Default ASS file
ScriptType: v4.00+
WrapStyle: 2
Collisions: Normal
PlayResX: 960
PlayResY: 720
ScaledBorderAndShadow: yes
Video Zoom Percent: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1
Style: left_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,1,10,10,5,1
Style: right_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,3,10,10,5,1
Style: left_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,7,10,10,5,1
Style: right_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,9,10,10,5,1
Style: center_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,8,10,10,5,1
Style: center_up_big,微软雅黑,28,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,8,10,10,5,1
Style: center_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1
Style: center_down_big,微软雅黑,28,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
        pass

    #生成播放时的背景字幕
    #filename：文件名
    #info：文件信息，用于左下角显示用的
    #out：文件路径
    def make_ass(self, info, out):
        info_txt = ''
        if info['type'] == 'id':
            info_txt = '当前网易云歌曲 ID：'+str(info['info']['id'])+'\\N歌手：'+info['info']['singer']+'\\N歌名：'+info['info']['name']+'\\N专辑：'+info['info']['alname']+'\\N点播人：'+info['username']+'\\N点播日期：'+info['time']
        elif info['type'] == 'mv':
            info_txt = '当前网易云MV ID：'+str(info['info']['id'])+'\\N歌手：'+info['info']['singer']+'\\NMV名：'+info['info']['name']+'\\N点播人：'+info['username']+'\\N点播日期：'+info['time']
        elif info['type'] == 'av':
            pass 
        file_content = self.ass_head+'''Dialogue: 2,0:00:00.00,01:00:00.00,left_down,,0,0,0,,'''+info_txt+'''
Dialogue: 2,0:00:00.00,01:00:00.00,right_down,,0,0,0,,基于树莓派3B
Dialogue: 2,0:00:00.00,01:00:00.00,left_up,,0,0,0,,树莓派点播台~\\N已开源，源码见https://biu.ee/pi-live/\\N使用时请保留源码链接
Dialogue: 2,0:00:00.00,01:00:00.00,right_up,,0,0,0,,弹幕点播方法请看直播间简介哦~
Dialogue: 2,0:00:00.00,0:00:00.00,right_up,,0,0,0,,测试点播台，功能不断完善中
'''
        file = open(out, 'w')    #保存ass字幕文件
        file.write(file_content)
        file.close()

    #生成歌词字幕文件
    def make_lrc_ass(self, filename, ass = '', asst = ''):
        ass = self.lrc_to_ass(ass)
        asst = self.tlrc_to_ass(asst)
        file_content = self.ass_head+ass+asst
        file = open(filename, 'w')    #保存ass字幕文件
        file.write(file_content)
        file.close()
        
    #滚动歌词生成
    def lrc_to_ass(self, lrc):
        lrc=lrc.splitlines() #按行分割开来
        list1=['00','00']
        list2=['00','00']
        list3=['00','00']
        list4=[' ',' ']
        result='\r\n'
        for i in lrc:
            matchObj = re.match( r'.*\[(\d+):(\d+)\.(\d+)\]([^\[\]]*)', i)  #正则匹配获取每行的参数，看不懂的去自行学习正则表达式
            if matchObj:    #如果匹配到了东西
                list1.append(matchObj.group(1))
                list2.append(matchObj.group(2))
                list3.append(matchObj.group(3))
                list4.append(matchObj.group(4))
        list1.append('05')
        list1.append('05')
        list2.append('00')
        list2.append('00')
        list3.append('00')
        list3.append('00')
        list4.append(' ')
        list4.append(' ')
        for i in range(2, len(list1)-4):
            text='　'+list4[i+1]+'　\\N　'+list4[i+2]+'　'
            result+='Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
            text='　'+list4[i]+'　'
            result+='Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_down_big,,0,0,0,,'+text+'\r\n'
            text='　'+list4[i-2]+'　\\N　'+list4[i-1]+'　'
            result+='Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
        #修正倒数第二句句歌词消失的bug
        text='　'+list4[len(list1)-3]+'　\\N　'+list4[len(list1)-2]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-4]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_down_big,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-6]+'　\\N　'+list4[len(list1)-5]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
        #修正最后一句歌词消失的bug
        text='　'+list4[len(list1)-2]+'　\\N　'+list4[len(list1)-1]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_down,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-3]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_down_big,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-5]+'　\\N　'+list4[len(list1)-4]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_down,,0,0,0,,'+text+'\r\n'
        return result


    #滚动歌词生成
    def tlrc_to_ass(self, lrc):
        lrc=lrc.splitlines() #按行分割开来
        list1=['00','00']
        list2=['00','00']
        list3=['00','00']
        list4=[' ',' ']
        result='\r\n'
        for i in lrc:
            matchObj = re.match( r'.*\[(\d+):(\d+)\.(\d+)\]([^\[\]]*)', i)  #正则匹配获取每行的参数，看不懂的去自行学习正则表达式
            if matchObj:    #如果匹配到了东西
                list1.append(matchObj.group(1))
                list2.append(matchObj.group(2))
                list3.append(matchObj.group(3))
                list4.append(matchObj.group(4))
        list1.append('05')
        list1.append('05')
        list2.append('00')
        list2.append('00')
        list3.append('00')
        list3.append('00')
        list4.append(' ')
        list4.append(' ')
        for i in range(2, len(list1)-4):
            text='　'+list4[i-2]+'　\\N　'+list4[i-1]+'　'
            result+='Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_up,,0,0,0,,'+text+'\r\n'
            text='　'+list4[i]+'　'
            result+='Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_up_big,,0,0,0,,'+text+'\r\n'
            text='　'+list4[i+1]+'　\\N　'+list4[i+2]+'　'
            result+='Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_up,,0,0,0,,'+text+'\r\n'
        #修正倒数第二句句歌词消失的bug
        text='　'+list4[len(list1)-6]+'　\\N　'+list4[len(list1)-5]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_up,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-4]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_up_big,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-3]+'　\\N　'+list4[len(list1)-2]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_up,,0,0,0,,'+text+'\r\n'
        #修正最后一句歌词消失的bug
        text='　'+list4[len(list1)-5]+'　\\N　'+list4[len(list1)-4]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_up,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-3]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_up_big,,0,0,0,,'+text+'\r\n'
        text='　'+list4[len(list1)-2]+'　\\N　'+list4[len(list1)-1]+'　'
        result+='Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_up,,0,0,0,,'+text+'\r\n'
        return result