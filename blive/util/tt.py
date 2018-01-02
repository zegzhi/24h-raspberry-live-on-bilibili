from util.AES import AESCipher
import json
import time
import urllib
import urllib.request

class NeteaseMusic(object):

    def __init__(self):
        self.config = {
            'nonce': '0CoJUm6Qyw8W8jud',
            'secretKey': 'TA3YiYCfY2dDJQgg',
            'encSecKey': '84ca47bca10bad09a6b04c5c927ef077d9b9f1e37098aa3eac6ea70eb59df0aa28b691b7e75e4f1f9831754919ea784c8f74fbfadf2898b0be17849fd656060162857830e241aba44991601f137624094c114ea8d17bce815b0cd4e5b8e2fbaba978c6d1d14dc3d1faf852bdd28818031ccdaaa13a6018e1024e2aae98844210',
            'IV': '0102030405060708',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.157 Safari/537.36',
                'Referer': 'http://music.163.com/',
                'Cookie': 'os=pc; osver=Microsoft-Windows-10-Professional-build-10586-64bit; appver=2.0.3.131777; channel=netease; __remember_me=true'
            }
        }
        
    # CURL
    def curl(self, url, data=None):
        params = self.prepare(data)
        headers = self.config['headers']
        postData = urllib.parse.urlencode(params).encode('utf-8')
        request = urllib.request.Request(url=url, data=postData, headers=headers, method='POST')
        response = json.loads(urllib.request.urlopen(request, timeout=10).read().decode('utf-8'))
        return response
        
    # aes-128-cbc
    def aesEncode(self, data, key):
        return AESCipher(key=key).encrypt(data, self.config['IV'])
    
    # 预处理Post数据
    def prepare(self, data):
        result = { 'params': self.aesEncode(json.dumps(data), self.config['nonce']) }
        result['params'] = self.aesEncode(result['params'], self.config['secretKey'])
        result['encSecKey'] = self.config['encSecKey']
        return result

    # 通过ID获取歌曲信息
    def getInfo(self, id):
        response = self.curl(url='http://music.163.com/weapi/v3/song/detail?csrf_token=', data={
            'c': json.dumps([{ 'id': id }]),
            'csrf_token': ''
        })
        if 'code' in response and response['code'] == 200:
            if 'songs' in response and response['songs']:
                song = response['songs'][0]
                return {
                    'id': song['id'],                    # id
                    'name': song['name'],                # 歌名
                    'singer': song['ar'][0]['name'],     # 歌手名
                    'alname': song['al']['name']         # 专辑名
                }
                pass
            else:
                return False
        else:
            return False
        
    # 通过ID获取MV信息
    def getMv(self, id):
        response = self.curl(url='http://music.163.com/weapi/mv/detail?csrf_token=', data={
            'id': id,
            'csrf_token': ''
        })
        if 'code' in response and response['code'] == 200:
            if 'data' in response and response['data']:
                data = response['data']
                return {
                    'id': data['id'],                    # id
                    'name': data['name'],                # 歌名
                    'singer': data['artistName'],        # 歌手名
                    'brs': data['brs']                   # 下载链接
                }
                pass
            else:
                return False
        else:
            return False