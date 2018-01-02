需求：
1.显示歌手和专题@修改下载服务器
5.删除命令
6.点播机回复过多@简化回复，反馈渲染进视频
7.和谐词处理

bug：
1.视频标题太长会遮挡字幕@换行
3.切歌时会卡顿@增加缓存池
4.误发命令@规范化命令
7.下载出错没反馈
8.只有mp4格式的视频无法点播 例：av17092740


测试数据：

kill `ps a|grep 'ffmpeg -re'|grep -v 'sh'|grep -v 'grep'|awk '{print $1}'`

id=579954
id=809268
点歌=恋爱サーキュレーション
mv=5682038

playlist=1996426579

id
mv
vedio

info{
    id
    name
    +
}

mu{
    singer
    alname
    lrc
}

mv{
    singer
    brs
}

PlayQueue{
    str:type
    obj:info
    str:username
    str:time
}

DownloadQueue{
    type
    info
    username
    time
}