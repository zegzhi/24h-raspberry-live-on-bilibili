import os
import random
import subprocess
import time

from service.Service import Service
from util.Queue import PlayQueue
from util.Config import Config
from util.Danmu import Danmu
from util.FFmpeg import *
from util.Log import Log
from util.AssMaker import *

class MediaService(Service):
    
    def __init__(self):
        self.danmu = Danmu()
        self.log = Log('Media Service')
        self.config = Config()
        self.ass = AssMaker()

    def run(self):
        try:
            # 判断队列是否为空
            if PlayQueue.empty():
                time.sleep(3)
                # 获取随机文件，播放
                musicPath = './resource/music/'
                musicName = self.getRandomFile(musicPath, '.mp3')
                # musicName = os.path.basename(musicName)
                musicName = os.path.splitext(musicName)[0]
                task = {}
                # 存在详情文件
                if os.path.isfile('%s%s.mp3.json' % (musicPath, musicName)):
                    f = open('%s%s.mp3.json' % (musicPath, musicName), 'rt')
                    task = json.loads(f.read())
                    f.close()
                else:
                    pass
                self.playMusic(task)
            else:
                # 获取新的下载任务
                task = PlayQueue.get()
                if task and 'type' in task:
                    if task['type'] == 'id':
                        self.playMusic(task)
                    elif task['type'] == 'mv':
                        self.playVedio(task)
                        pass
        except Exception as e:
            self.log.error(e)
    
    # 播放音乐
    def playMusic(self, music):
        self.log.info('[Music] 开始播放[%s]点播的[%s]' % (music['username'], music['info']['name']))
        self.danmu.send('正在播放%s' % music['info']['name'])
        # 生成背景字幕
        self.ass.make_ass(music, './resource/bak.ass')
        # 处理图片
        imagePath = './resource/img/'
        randomImage = imagePath + self.getRandomFile(imagePath)
        command = ffmpeg().getImage(image=randomImage, output='./resource/bak.jpg', ass='./resource/bak.ass')
        command = "%s 2>> ./log/ffmpeg_img.log" % command
        self.log.debug(command)
        process = subprocess.Popen(args=command, cwd=os.getcwd(), shell=True)
        process.wait()
        # 获取歌词
        assPath = ''
        if 'lrc' in music['info']:
            assPath = './resource/music/%s.mp3.ass' % music['info']['id']
        # 开始播放
        mp3Path = './resource/music/%s.mp3' % music['info']['id']
        command = ffmpeg().getMusic(music=mp3Path, output=self.getRTMPUrl(), image='./resource/bak.jpg', ass=assPath)
        command = "%s 2>> ./log/ffmpeg.log" % command
        self.log.debug(command)
        process = subprocess.Popen(args=command, cwd=os.getcwd(), shell=True)
        process.wait()
        self.log.info('[Music] [%s]播放结束' % music['info']['name'])
    
    # 播放视频
    def playVedio(self, music):
        self.log.info('[Music] 开始播放[%s]点播的[%s]' % (music['username'], music['info']['name']))
        self.danmu.send('正在播放%s' % music['info']['name'])
        # 开始播放
        vedioPath = './resource/video/%s_mv.flv' % music['info']['id']
        command = ffmpeg().getVedio(vedio=vedioPath, output=self.getRTMPUrl())
        command = "%s 2>> ./log/ffmpeg.log" % command
        self.log.debug(command)
        process = subprocess.Popen(args=command, cwd=os.getcwd(), shell=True)
        process.wait()
        self.log.info('[Music] [%s]播放结束' % music['info']['name'])

    # 获取推流地址
    def getRTMPUrl(self):
        url = self.config.get(module='rtmp', key='url')
        code = self.config.get(module='rtmp', key='code')
        return url + code

    # 获取随机文件
    def getRandomFile(self, path, type=None):
        fileList = []
        if type:
            for filename in os.listdir(path):
                if os.path.splitext(filename)[1] == type:
                    fileList.append(filename)
        else:
            fileList = os.listdir(path)
        if len(fileList) == 0:
            raise Exception('无法获取随机文件，%s为空' % path)
        index = random.randint(0, len(fileList) - 1)
        return fileList[index]
