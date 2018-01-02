from service.Service import Service
from util.NeteaseMusic import *
from util.Danmu import Danmu
from util.Log import Log
from util.Queue import DownloadQueue
from util.Config import Config
import time
import os

class DanmuService(Service):
    
    def __init__(self):
        self.danmu = Danmu()
        self.config = Config()
        self.neteaseMusic = NeteaseMusic()
        self.log = Log('Danmu Service')
        self.commandMap = {
            '点歌=': 'selectSongAction',
            'id=': 'selectSongByIdAction',
            'mv=': 'selectMvByIdAction',
            '切歌': 'DebugAction'
        }
        pass

    def run(self):
        try:
            self.parseDanmu()
            time.sleep(1.5)
        except Exception as e:
            self.log.error(e)

    # 解析弹幕
    def parseDanmu(self):
        danmuList = self.danmu.get()
        if danmuList:
            for danmu in danmuList:
                self.log.debug('%s: %s' % (danmu['name'], danmu['text']))
                if danmu['name'] != self.config.get('miaoUser'):  # 不响应弹幕姬的弹幕
                    danmu['text'] = danmu['text'].replace(' ','')     # 删除空格防和谐
                    self.danmuStateMachine(danmu)
        pass

    # 将对应的指令映射到对应的Action上
    def danmuStateMachine(self, danmu):
        text = danmu['text']
        commandAction = ''
        for key in self.commandMap:
            # 遍历查询comand是否存在 若存在则反射到对应的Action
            if text.find(key) == 0 and hasattr(self, self.commandMap[key]):
                danmu['command'] = danmu['text'][len(key) : len(danmu['text'])]
                getattr(self, self.commandMap[key])(danmu)
                break
        pass

    # 歌曲名点歌
    def selectSongAction(self, danmu):
        self.log.info('%s 点歌 [%s]' % (danmu['name'], danmu['command']))
        command = danmu['command']
        song = []
        # 按歌曲名-歌手点歌
        if command.find('-') != -1:
            detail = command.split('-')
            if len(detail) == 2:
                song = self.neteaseMusic.searchSingle(detail[0], detail[1])
            else:
                # 查询失败
                song = {}
        # 直接按歌曲名点歌
        else:
            song = self.neteaseMusic.searchSingle(danmu['command'])

        if song:
            self.danmu.send('%s点歌成功' % song['name'])
            DownloadQueue.put({
                    'type': 'id',
                    'info': song,
                    'username': danmu['name'],
                    'time': danmu['time']
                })
        else:
            # 未找到歌曲
            self.danmu.send('找不到%s' % danmu['command'])
            self.log.info('找不到%s' % danmu['command'])

    # 通过Id点歌
    def selectSongByIdAction(self, danmu):
        self.log.info('%s ID [%s]' % (danmu['name'], danmu['command']))
        command = danmu['command']
        try:
            song = self.neteaseMusic.getInfo(command)
            if song:
                self.danmu.send('%s点歌成功' % song['name'])
                DownloadQueue.put({
                        'type': 'id',
                        'info': song,
                        'username': danmu['name'],
                        'time': danmu['time']
                    })
            else:
                # 未找到歌曲
                raise Exception('未找到歌曲')
        except Exception as e:
            self.danmu.send('找不到%s' % danmu['command'])
            self.log.info('找不到%s' % danmu['command'])
    
    # 通过Id点Mv
    def selectMvByIdAction(self, danmu):
        self.log.info('%s MV [%s]' % (danmu['name'], danmu['command']))
        command = danmu['command']
        try:
            mv = self.neteaseMusic.getMv(command)
            if mv:
                self.danmu.send('%s点播成功' % mv['name'])
                DownloadQueue.put({
                        'type': 'mv',
                        'info': mv,
                        'username': danmu['name'],
                        'time': danmu['time']
                    })
            else:
                # 未找到歌曲
                raise Exception('未找到MV')
        except Exception as e:
            self.danmu.send('找不到%s' % danmu['command'])
            self.log.info('找不到%s' % danmu['command'])
            
    def DebugAction(self, danmu):
        if danmu['name'] in self.config.get('adminUser'):
            if danmu['text'] == '切歌':
                os.system("kill `ps a|grep 'ffmpeg -re'|grep -v 'sh'|grep -v 'grep'|awk '{print $1}'`")
                self.danmu.send('切歌成功')