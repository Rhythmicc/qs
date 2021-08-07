# coding=utf-8
"""
功能映射与菜单提示

Function mapping and menu prompt
"""
from . import user_lang, qs_default_console
from .qsLesson import lesson


def color_rep(ss, is_top_menu: bool = False):
    """
    格式化菜单文本（添加颜色）

    Format menu text (add color)

    :param is_top_menu:
    :param ss: 文本
    :return: 处理后的文本
    """
    from rich.table import Table, Column
    from rich.box import SIMPLE
    ss = ss.strip().split('\n')

    tb = Table(
        *([Column('1', style='bold magenta', justify='left'), Column('2', style='bold yellow', justify='center'),
           Column('3', style='bold green', justify='right')] if is_top_menu else
          [Column('1', style='bold magenta', justify='left'), Column('2', style='bold yellow', justify='right')]),
        title=f'[bold underline]{"QuickStart_Rhy" if is_top_menu else ss[0].strip().strip(":")}' + '\n',
        show_header=False, show_edge=False, box=SIMPLE
    )
    for i, line in enumerate(ss if is_top_menu else ss[1:]):
        if ':->' in line:
            line = [i.strip() for i in line.split(':->')]
            if '|' in line[1]:
                line += [i.strip() for i in line.pop(-1).split('|')]
        tb.add_row(*line)
    qs_default_console.print(tb, justify="center")


def base_menu():
    """基础类菜单 | Basic menu"""
    color_rep("""Basic Tools help:
    qs u   <url...>          :-> open urls using default browser
    qs a   <app> \[file..]    :-> open app or open file by app(for Mac OS)
    qs f   <file...>         :-> open file by default app
    qs cal <exp>             :-> calculate exp
    qs time                  :-> view current time
    qs pact                  :-> output string in clipboard
    qs fcopy <file>          :-> copy file content to clipboard""") \
        if user_lang != 'zh' else color_rep("""基础工具:
    qs u   <url...>          :-> 使用默认浏览器打开多个链接
    qs a   <app> \[file..]    :-> 打开应用或使用应用打开文件 (仅支持Mac OS)
    qs f   <file...>         :-> 使用合适的应用打开文件
    qs cal <exp>             :-> 计算算术表达式
    qs time                  :-> 查看当前时间
    qs pcat                  :-> 输出粘贴板内容
    qs fcopy <file>          :-> 拷贝文件内容到粘贴板""")


def system_menu():
    """系统类菜单 | System menu"""
    color_rep("""System Tools help:
    qs top                   :-> cpu and memory monitor
    qs clear                 :-> free memory
    qs go2git                :-> go to the webpage of the git config
    qs mktar  <path...>      :-> create gzipped archive for path
    qs untar  <path...>      :-> extract *.tar.*
    qs mkzip  <path...>      :-> make a zip for path
    qs unzip  <path...>      :-> extract *.zip file
    qs unrar  <path...>      :-> extract *.rar file
    qs mk7z   <path...>      :-> make a 7z archive for path
    qs un7z   <path...>      :-> extract *.7z file
    qs md5    <path...>      :-> calculate md5 of files
    qs sha1   <path...>      :-> calculate SHA1 of files
    qs sha256 <path...>      :-> calculate SHA256 of files
    qs sha512 <path...>      :-> calculate SHA512 of files
    qs diff <dir1> <dir2>    :-> diff two directories""") \
        if user_lang != 'zh' else color_rep("""系统工具:
    qs top                   :-> CPU和内存监控器
    qs clear                 :-> 清理本机内存
    qs go2git                :-> 自动前往git目录托管仓库的网页
    qs mktar  <path...>      :-> 使用多个文件或文件夹创建tar压缩包
    qs untar  <path...>      :-> 解压各种格式的tar包
    qs mkzip  <path...>      :-> 使用多个文件或文件夹创建zip压缩包
    qs unzip  <path...>      :-> 解压zip压缩包
    qs unrar  <path...>      :-> 解压rar压缩包
    qs mk7z   <path...>      :-> 使用多个文件或文件夹创建7z 压缩包
    qs un7z   <path...>      :-> 解压7z 压缩包
    qs md5    <path...>      :-> 计算文件的md5值
    qs sha1   <path...>      :-> 计算文件sha1值
    qs sha256 <path...>      :-> 计算文件sha256值
    qs sha512 <path...>      :-> 计算文件sha512值
    qs diff <dir1> <dir2>    :-> 对比两个文件夹差异""")


def net_menu():
    """网络类菜单 | Network menu"""
    color_rep("""Net Tools help:
    qs http \[ip] [-bind url] :-> start a multithread ftp server
    qs netinfo [<domains>..] :-> get url's info which in clipboard or params 
    qs dl [urls] [-help]     :-> download file from url(in clipboard)
    qs wifi                  :-> connect wifi
    qs upload                :-> upload your pypi library
    qs upgrade               :-> update qs""") \
        if user_lang != 'zh' else color_rep("""网络工具:
    qs http \[ip] [-bind url] :-> 在当前路径下开启多线程http服务
    qs netinfo [<domains>..] :-> 获取命令参数或剪切板中链接或ip的信息 
    qs dl [urls]             :-> 从命令参数或剪切板中链接下载文件
    qs wifi                  :-> 连接wifi
    qs upload                :-> 上传你的pypi仓库
    qs upgrade               :-> 更新qs""")


def api_menu():
    """api类菜单 | API menu"""
    color_rep("""API Tools help:
    qs trans  \[content]       :-> translate the content(in clipboard)
    qs pinyin \[content]      :-> get the pinyin of Chinese content
    qs rmbg   <img>            :-> remove image background
    qs smms   <img/*.md>       :-> upload img or img in markdown to sm.ms
    qs upimg  -help          :-> upload img or img in markdown to platform
    qs alioss -help          :-> get aliyun oss api help menu
    qs txcos  -help          :-> get tencent cos api help menu
    qs qiniu  -help          :-> get qiniu oss api help menu
    qs weather \[address]     :-> check weather (of address)
    qs LG  <image>            :-> make image larger(with AI)
    qs nlp \[words]           :-> Text(or in clipboard) error correction
    qs cb  <method> \[msg]     :-> Get Or Post msg by using network disk
    qs pasteme <method> [*]  :-> get with key, [password] or post clipboard content
    qs bcv   <url/video code> :-> get Bilibili video cover image with <url>
    qs gbc   <garbage...>     :-> check Chinese garbage classification
    qs svi   <url> \[-url]     :-> get short video info (show url)
    qs svd   <url>            :-> download short video info as mp4
    qs acg   [-save]          :-> get an acg image link (or save)
    qs photo [-save]          :-> get an porn photo link (or save)
    qs bing  [-save]          :-> get an bing image link (or save)
    qs phi   <url>            :-> get <image url> in url (preview on Mac)
    qs kd    <courier number> :-> Query China express
    qs loli  [-save] [-p]    :-> get and loli image link [or save (use default proxy)]
    qs setu  [-save] [-p]    :-> randomly call acg, acg2, loli
    qs exc  <num> <to> \[fr]  :-> Query <number> <fr> corresponding <number?> <to>
    qs zhihu                 :-> Get zhihu.com Daily
    qs wallhaven [-save]     :-> Get Wallhaven Toplist
    qs lmgtfy <keywords>     :-> Get LMGTFY link for keywords
    qs d60                   :-> Get the daily 60-second morning report""")\
        if user_lang != 'zh' else color_rep("""API工具:
    qs trans  \[content]       :-> 翻译命令参数或剪切板中的内容
    qs pinyin \[content]      :-> 获取中文内容的拼音
    qs rmbg   <img>            :-> 移除图片背景
    qs smms   <img/*.md>       :-> 将图片或Markdown中图片上传至sm.ms
    qs upimg  -help          :-> 将图片或Markdown中图片上传至多平台（暂无需token）
    qs alioss -help          :-> 获取阿里云对象存储的使用帮助
    qs txcos  -help          :-> 获取腾讯云对象存储的使用帮助
    qs qiniu  -help          :-> 获取七牛云对象存储的使用帮助
    qs weather \[address]     :-> 获取当地天气（或指定地址天气）
    qs LG  <image>            :-> 通过百度图像效果增强放大图片
    qs nlp \[words]           :-> 通过百度NLP进行文本纠错
    qs cb  <method> \[msg]     :-> 通过网络硬盘的本地文件系统get或post信息
    qs pasteme <method> [*]  :-> 通过pasteme get或post信息
    qs bcv   <url/video code> :-> 获取B站视频、直播封面图片
    qs gbc   <garbage...>     :-> 查询垃圾分类
    qs svi   <url> \[-url]     :-> 获取多平台短视频信息 (展示链接)
    qs svd   <url>            :-> 下载多平台短视频为mp4
    qs acg   [-save]          :-> 获取一张acg图片链接 (或保存)
    qs photo [-save]          :-> 获取一张涩图链接 (或保存)
    qs bing  [-save]          :-> 获取一张bing图片链接 (或保存)
    qs phi   <url>            :-> 获取url里的图片链接 (Mac上iTerm可预览)
    qs kd    <courier number> :-> 查询国内快递
    qs loli  [-save] [-p]     :-> 获取一张萝莉图片链接 [或(使用默认代理)下载]
    qs setu  [-save] [-p]     :-> 随机调用acg, acg2, loli
    qs exc <num> <to> \[fr]   :-> 汇率查询<number> <fr> 对应 多少 <to>
    qs zhihu                :-> 获取知乎日报
    qs wallhaven [-save]     :-> 获取Wallhaven Top动漫涩图
    qs lmgtfy <keywords>     :-> 获取关键词的LMGTFY链接
    qs d60                   :-> 获取每日60秒早报""")


def image_menu():
    """图像处理类菜单 | Image Deal Menu"""
    color_rep("""Image Tools help:
    qs stbg <pic> <to> \[from]    :-> color replace for picture
    qs icat <img>            :-> preview image on terminal
    qs v2gif <path> \[sz] \[fps] :-> generate gif from video
    qs v2mp4 <video>         :-> format video to mp4
    qs v2mp3 <video>         :-> extract audio from video and save in MP3
    qs rmaudio <video>       :-> remove audio in video (return mp4 only)
    qs i2png <imgs...>       :-> transform imgs to png
    qs i2jpg <imgs...>       :-> transform imgs to jpg
    qs fmti <pic> <to> \[exp...] :-> format image to <to> color except \[exp...] color""") \
        if user_lang != 'zh' else color_rep("""图像处理:
    qs stbg    <pic> <to> \[from]    :-> 替换图片颜色 (from默认为透明)
    qs icat    <img>            :-> 在终端预览图片
    qs v2gif   <path> \[sz] \[fps] :-> 将视频导出为gif
    qs v2mp4   <video>         :-> 将视频导出为mp4
    qs v2mp3   <video>         :-> 提取视频音频为mp3
    qs rmaudio <video>       :-> 删除mp4文件音频
    qs i2png   <imgs...>       :-> 将图像转换为png
    qs i2jpg   <imgs...>       :-> 将图像转换为jpg
    qs fmti    <pic> <to> \[exp...] :-> 格式化图片颜色为<to>，忽略\[exp...]颜色""")


menu_table = {
    'basic': base_menu,
    'system': system_menu,
    'net': net_menu,
    'api': api_menu,
    'image': image_menu,
    'lesson': lesson
}

basic_funcs = {
    'self': 'basic',
    'u': 'u',
    'a': 'open_app',
    'f': 'open_file',
    'i': 'init',
    'time': 'cur_time',
    'cal': 'calculate',
    'pcat': 'pcat',
    'fcopy': 'fcopy'
}

system_funcs = {
    'self': 'system',
    'top': 'top',
    'clear': 'clear_mem',
    'go2git': 'go_github',
    'mktar': 'mktar',
    'untar': 'untar',
    'mkzip': 'mkzip',
    'unzip': 'unzip',
    'unrar': 'unrar',
    'mk7z': 'mk7z',
    'un7z': 'un7z',
    'md5': 'md5',
    'sha1': 'sha1',
    'sha256': 'sha256',
    'sha512': 'sha512',
    'diff': 'diff_dir'
}

net_funcs = {
    'self': 'netTools',
    'http': 'http',
    'dl': 'download',
    'wifi': 'wifi',
    'upgrade': 'upgrade',
    'upload': 'upload_pypi',
    'netinfo': 'netinfo'
}

api_funcs = {
    'self': 'api',
    'trans': 'translate',
    'pinyin': 'pinyin',
    'rmbg': 'remove_bg',
    'smms': 'smms',
    'upimg': 'up_img',
    'alioss': 'ali_oss',
    'qiniu': 'qiniu',
    'txcos': 'txcos',
    'LG': 'largeImage',
    'weather': 'weather',
    'nlp': 'AipNLP',
    'cb': 'CommonClipboard',
    'pasteme': 'Pasteme',
    'bcv': 'bili_cover',
    'gbc': 'gbc',
    'svi': 'short_video_info',
    'svd': 'short_video_dl',
    'acg': 'acg',
    'bing': 'bingImg',
    'phi': 'preview_html_images',
    'kd': 'kdCheck',
    'loli': 'loli',
    'photo': 'photo',
    'setu': 'setu',
    'exc': 'exchange',
    'zhihu': 'zhihuDaily',
    'wallhaven': 'wallhaven',
    'lmgtfy': 'lmgtfy',
    'd60': 'daily60s'
}

image_funcs = {
    'self': 'imageDeal',
    'stbg': 'set_img_background',
    'icat': 'icat',
    'v2gif': 'v2gif',
    'rmaudio': 'remove_audio',
    'v2mp4': 'v2mp4',
    'v2mp3': 'v2mp3',
    'i2png': 'i2png',
    'i2jpg': 'i2jpg',
    'fmti': 'fmt_img_color'
}
