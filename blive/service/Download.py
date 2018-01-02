from util.Queue import DownloadQueue, PlayQueue
from util.NeteaseMusic import NeteaseMusic
from service.Service import Service
from util.Danmu import Danmu
from util.Log import Log
from util.AssMaker import AssMaker
from util.Request import Request
from util.AssMaker import *
from util.FFmpeg import *
import subprocess
import json
import os

class DownloadService(Service):

    def __init__(self):
        self.danmu = Danmu()
        self.ass = AssMaker()
        self.log = Log('Download Service')
        self.neteaseMusic = NeteaseMusic()

    # 获取下载队列 分发至下载函数
    def run(self):
        try:
            # 判断队列是否为空
            if DownloadQueue.empty():
                return
            # 获取新的下载任务
            task = DownloadQueue.get()
            if task and 'type' in task:
                self.download(task)
                PlayQueue.put(task)
                self.log.info('播放列表+1')
        except Exception as e:
            self.log.error(e)
            
    # 下载媒体
    def download(self, info, filename=None, callback=None):
        self.danmu.send('正在下载%s' % info['info']['name'])
        # 名称处理
        if not filename:
            filename = info['info']['id']
        if info['type'] == 'id':
            songId = info['info']['id']
            # 本地不存在此歌曲
            if (str(songId)+'.mp3') not in os.listdir('./resource/music/'):
                # 下载歌曲
                musicUrl = self.neteaseMusic.getSingleUrl(songId)
                mp3_filename = './resource/music/%s.mp3' % filename
                Request.download(musicUrl, mp3_filename, callback)
                # 获取歌词文件
                lyric = self.neteaseMusic.getLyric(songId)
                if lyric:
                    ass_filename = '%s.ass' % mp3_filename
                    self.ass.make_lrc_ass(ass_filename, lyric['lyric'], lyric['tlyric'])
                    info['info']['lrc'] = True
                else:
                    info['info']['lrc'] = False
                # 保存点歌信息
                file = open('%s.json' % mp3_filename, 'w')
                file.write(json.dumps(info,ensure_ascii=False))
                file.close()
                self.log.info('歌曲下载完毕 %s - %s' % (info['info']['name'], info['info']['singer']))
            else:
                # 更新点歌信息
                pass
            return filename
        elif info['type'] == 'mv':
            mvId = info['info']['id']
            # 本地不存在此mv
            if (str(mvId)+'_mv.flv') not in os.listdir('./resource/video/'):
                # 下载mv
                mvUrl = ''
                if '720' in info['info']['brs']:
                    mvUrl = info['info']['brs']['720']
                elif '480' in info['info']['brs']:
                    mvUrl = info['info']['brs']['480']
                else:
                    return None
                downPath = './resource/video/%s_mv.down' % filename
                Request.download(mvUrl, downPath, callback)
                self.log.info('MV下载完毕 %s - %s' % (info['info']['name'], info['info']['singer']))
                # 生成背景字幕
                self.ass.make_ass(info, './resource/video/bak.ass')
                # 渲染MV
                renderPath = './resource/video/%s_mv.render' % filename
                command = ffmpeg().renderVedio(vedio=downPath, output=renderPath, ass='./resource/video/bak.ass')
                command = "%s 2>> ./log/ffmpeg.log" % command
                self.log.debug(command)
                process = subprocess.Popen(args=command, cwd=os.getcwd(), shell=True)
                process.wait()
                # 渲染完成，修改文件名
                os.remove(downPath)
                mp4Path = './resource/video/%s_mv.flv' % filename
                os.rename(renderPath, mp4Path)
                # 保存点歌信息
                file = open('%s.json' % mp4Path, 'w')
                file.write(json.dumps(info,ensure_ascii=False))
                file.close()
                self.log.info('MV渲染完毕 %s - %s' % (info['info']['name'], info['info']['singer']))
            else:
                # 更新点歌信息
                pass
            return filename

