# coding=utf-8
from QuickStart_Rhy import user_lang
import colorama
from colorama import Fore, Style
colorama.init()


def color_rep(ss):
    """
    格式化菜单文本（添加颜色）

    Format menu text (add color)

    :param ss: 文本
    :return: 处理后的文本
    """
    ss = ss.strip('\n').split('\n')
    for i, line in enumerate(ss):
        if ':->' in line:
            line = line.split(':->')
            line = Fore.LIGHTMAGENTA_EX + line[0] + Style.RESET_ALL + ':->' + Fore.YELLOW + line[1] + Style.RESET_ALL
        if '|' in line:
            line = line.split('|')
            line = line[0] + Style.RESET_ALL + '|' + Fore.GREEN + line[1] + Style.RESET_ALL
        ss[i] = line
    return '\n'.join(ss)


def base_menu():
    """基础类菜单 | Basic menu"""
    print(color_rep("""Basic Tools help:
    qs -u  <url...>           :-> open urls using default browser
    qs -a  <app> [file..]     :-> open app or open file by app(for Mac OS)
    qs -f  <file...>          :-> open file by default app
    qs -cal exp               :-> calculate exp
    qs -time                  :-> view current time""")) \
        if user_lang != 'zh' else print(color_rep("""基础工具:
    qs -u  <url...>           :-> 使用默认浏览器打开多个链接
    qs -a  <app> [file..]     :-> 打开应用或使用应用打开文件（仅支持Mac OS）
    qs -f  <file...>          :-> 使用合适的应用打开文件
    qs -cal exp               :-> 计算算术表达式
    qs -time                  :-> 查看当前时间"""))


def system_menu():
    """系统类菜单 | System menu"""
    print(color_rep("""System Tools help:
    qs -top                   :-> cpu and memory monitor
    qs -clear                 :-> free memory
    qs -mktar <path...>       :-> create gzipped archive for path
    qs -untar <path...>       :-> extract path.tar.*
    qs -mkzip <path...>       :-> make a zip for path
    qs -unzip <path...>       :-> extract *.zip file
    qs -unrar <path...>       :-> extract *.rar file""")) \
        if user_lang != 'zh' else print(color_rep("""系统工具:
    qs -top                   :-> CPU和内存监控器
    qs -clear                 :-> 清理本机内存
    qs -mktar <path...>       :-> 使用多个文件或文件夹创建tar压缩包
    qs -untar <path...>       :-> 解压各种格式的tar包
    qs -mkzip <path...>       :-> 使用多个文件或文件夹创建zip压缩包
    qs -unzip <path...>       :-> 解压zip压缩包
    qs -unrar <path...>       :-> 解压rar压缩包"""))


def net_menu():
    """网络类菜单 | Network menu"""
    print(color_rep("""Net Tools help:
    qs -http [ip] [-bind url] :-> start a multithread ftp server
    qs -netinfo [<domains>..] :-> get url's info which in clipboard or params 
    qs -dl [urls] [-help]     :-> download file from url(in clipboard)
    qs -upload                :-> upload your pypi library
    qs -upgrade               :-> update qs""")) \
        if user_lang != 'zh' else print(color_rep("""网络工具:
    qs -http [ip] [-bind url] :-> 在当前路径下开启多线程http服务
    qs -netinfo [<domains>..] :-> 获取命令参数或剪切板中链接或ip的信息 
    qs -dl [urls]             :-> 从命令参数或剪切板中链接下载文件
    qs -upload                :-> 上传你的pypi仓库
    qs -upgrade               :-> 更新qs"""))


def api_menu():
    """api类菜单 | API menu"""
    print(color_rep("""API Tools help:
    qs -trans [content]       :-> translate the content(in clipboard)
    qs -rmbg <img>            :-> remove image background
    qs -smms <img/*.md>       :-> upload img or img in markdown to sm.ms
    qs -upimg  -help          :-> upload img or img in markdown to platform
    qs -alioss -help          :-> get aliyun oss api help menu
    qs -txcos  -help          :-> get tencent cos api help menu
    qs -qiniu  -help          :-> get qiniu oss api help menu
    qs -weather [address]     :-> check weather (of address)
    qs -LG <image>            :-> make image larger(with AI)
    qs -nlp [words]           :-> Text(or in clipboard) error correction
    qs -sea <method> [msg]    :-> Get Or Post msg by Seafile.
    qs -pasteme <method> [*]  :-> get with key, [password] or post clipboard content
    qs -bcv <url/video code>  :-> get Bilibili video cover image with <url>
    qs -gbc <garbage...>      :-> check Chinese garbage classification
    qs -svi <url>             :-> get short video info
    qs -svd <url>             :-> download short video info as mp4
    qs -acg [save]            :-> get an acg image link (or save)"""))\
        if user_lang != 'zh' else print(color_rep("""API工具:
    qs -trans [content]       :-> 翻译命令参数或剪切板中的内容
    qs -rmbg <img>            :-> 移除图片背景
    qs -smms <img/*.md>       :-> 将图片或Markdown中图片上传至sm.ms
    qs -upimg  -help          :-> 将图片或Markdown中图片上传至多平台（暂无需token）
    qs -alioss -help          :-> 获取阿里云对象存储的使用帮助
    qs -txcos  -help          :-> 获取腾讯云对象存储的使用帮助
    qs -qiniu  -help          :-> 获取七牛云对象存储的使用帮助
    qs -weather [address]     :-> 获取当地天气（或指定地址天气）
    qs -LG <image>            :-> 通过百度图像效果增强放大图片
    qs -nlp [words]           :-> 通过百度NLP进行文本纠错
    qs -sea <method> [msg]    :-> 通过Seafile get或post信息
    qs -pasteme <method> [*]  :-> 通过pasteme get或post信息
    qs -bcv <url/video code>  :-> 获取B站视频、直播封面图片
    qs -gbc <garbage...>      :-> 查询垃圾分类
    qs -svi <url>             :-> 获取多平台短视频信息
    qs -svd <url>             :-> 下载多平台短视频为mp4
    qs -acg [save]            :-> 获取一张acg图片链接（或保存）"""))


def image_menu():
    """图像处理类菜单 | Image Deal Menu"""
    print(color_rep("""Image Tools help:
    qs -stbg pic to [from]    :-> color replace for picture
    qs -v2gif path [sz] [fps] :-> generate gif from video
    qs -v2mp4 <video>         :-> format video to mp4
    qs -v2mp3 <video>         :-> extract audio from video and save in MP3
    qs -rmaudio <video>       :-> remove audio in video (return mp4 only)""")) \
        if user_lang != 'zh' else print(color_rep("""图像处理:
    qs -stbg pic to [from]    :-> 替换图片颜色（from默认为透明）
    qs -v2gif path [sz] [fps] :-> 将视频导出为gif
    qs -v2mp4 <video>         :-> 将视频导出为mp4
    qs -v2mp3 <video>         :-> 提取视频音频为mp3
    qs -rmaudio <video>       :-> 删除mp4文件音频"""))


menu_table = {
    '-basic': base_menu,
    '-system': system_menu,
    '-net': net_menu,
    '-api': api_menu,
    '-image': image_menu
}


basic_funcs = {
    'self': 'basic',
    '-u': 'u',
    '-a': 'open_app',
    '-f': 'open_file',
    '-i': 'init',
    '-time': 'cur_time',
    '-cal': 'calculate'
}

system_funcs = {
    'self': 'system',
    '-top': 'top',
    '-clear': 'clear_mem',
    '-mktar': 'mktar',
    '-untar': 'untar',
    '-mkzip': 'mkzip',
    '-unzip': 'unzip',
    '-unrar': 'unrar'
}

net_funcs = {
    'self': 'nettools',
    '-http': 'http',
    '-dl': 'download',
    '-upgrade': 'upgrade',
    '-upload': 'upload_pypi',
    '-netinfo': 'netinfo'
}

api_funcs = {
    'self': 'api',
    '-trans': 'translate',
    '-rmbg': 'remove_bg',
    '-smms': 'smms',
    '-upimg': 'up_img',
    '-alioss': 'ali_oss',
    '-qiniu': 'qiniu',
    '-txcos': 'txcos',
    '-LG': 'largeImage',
    '-weather': 'weather',
    '-nlp': 'AipNLP',
    '-sea': 'Seafile_Communicate',
    '-pasteme': 'Pasteme',
    '-bcv': 'bili_cover',
    '-gbc': 'gbc',
    '-svi': 'short_video_info',
    '-svd': 'short_video_dl',
    '-acg': 'acg'
}

image_funcs = {
    'self': 'imagedeal',
    '-stbg': 'set_img_background',
    '-v2gif': 'v2gif',
    '-rmaudio': 'remove_audio',
    '-v2mp4': 'v2mp4',
    '-v2mp3': 'v2mp3'
}
