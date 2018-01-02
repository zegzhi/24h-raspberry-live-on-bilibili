from mutagen.mp3 import MP3

class ffmpeg(object):
    def __init__(self):
        pass

    def getImage(self, image, output, ass):
        ffmpegCommand = "ffmpeg -y -i '%s' -vf ass='%s' -pix_fmt yuv420p -f image2 '%s'" % (image, ass, output)
        return ffmpegCommand
        
    def getMusic(self, music, output, image='', ass=''):
        audio = MP3(music)
        audioTimeLength = str(int(audio.info.length))
        ffmpegCommand = ''
        if ass != '':
            ffmpegCommand = "ffmpeg -re -loop 1 -r 3 -t %s -f image2 -i '%s' -i '%s' -vf ass='%s' -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 3000k -c:a aac -b:a 192k -c:v h264_omx -f flv '%s'" % (audioTimeLength, image, music, ass, output)
        else:
            ffmpegCommand = "ffmpeg -re -loop 1 -r 3 -t %s -f image2 -i '%s' -i '%s' -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 3000k -c:a aac -b:a 192k -c:v h264_omx -f flv '%s'" % (audioTimeLength, image, music, output)
        return ffmpegCommand
        
    def getVedio(self, vedio, output, ass=''):
        ffmpegCommand = ''
        if ass != '':
            ffmpegCommand = "ffmpeg -re -i '%s' -vf ass='%s' -c:a copy -c:v copy -f flv '%s'" % (vedio, ass, output)
        else:
            ffmpegCommand = "ffmpeg -re -i '%s' -c:a copy -c:v copy -f flv '%s'" % (vedio, output)
        return ffmpegCommand

    def renderVedio(self, vedio, output, ass=''):
        if ass != '':
            ffmpegCommand = "ffmpeg -i '%s' -s 1280x720 -vf ass='%s' -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 3000k -c:a aac -b:a 192k -c:v libx264 -f flv '%s'" % (vedio, ass, output)
        else:
            ffmpegCommand = "ffmpeg -i '%s' -s 1280x720 -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 3000k -c:a aac -b:a 192k -c:v libx264 -f flv '%s'" % (vedio, output)
        return ffmpegCommand