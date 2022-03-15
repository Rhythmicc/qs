const completionSpec: Fig.Spec = {
  name: "qs",
  description: "QuickStart_Rhy--你的命令行助手",
  subcommands: [{
    name: 'basic',
    description: '基础工具帮助',
  }, {
    name: 'system',
    description: "系统工具帮助",
  }, {
    name: 'net',
    description: '网络工具帮助',
  }, {
    name: 'api',
    description: '扩展工具帮助',
  }, {
    name: 'image',
    description: '图像工具帮助',
  }, {
    name: 'u',
    description: '使用默认浏览器打开多个链接',
    args: {name: 'url', description: '链接', isVariadic: true}
  }, {
    name: 'a',
    description: '打开应用或使用应用打开文件(仅支持Mac)',
    args: [
        {name: 'app', description: '应用程序'},
        {name: 'files', description: '多个文件', isOptional: true, isVariadic: true, template: ['filepaths','folders']}
    ]
  }, {
    name: 'f',
    description: '使用默认应用打开文件',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'cal',
    description: '计算表达式',
    args: {name: 'exp', description: '表达式'}
  }, {
    name: 'time',
    description: '查看当前时间'
  }, {
    name: 'pcat',
    description: '输出粘贴板内容'
  }, {
    name: 'fcopy',
    description: '拷贝文件内容到粘贴板',
    args: {name: 'file', description: '文件', template: ['filepaths', 'folders']}
  }, {
    name: 'top',
    description: 'CPU和内存监控器',
  }, {
    name: 'clear',
    description: '清理内存',
    isDangerous:  true
  }, {
    name: 'go2git',
    description: '自动前往git目录托管仓库的网页'
  }, {
    name: 'mktar',
    description: '使用多个文件或文件夹创建tar压缩包',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'mkzip',
    description: '使用多个文件或文件夹创建zip压缩包',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'mk7z',
    description: '使用多个文件或文件夹创建7z压缩包',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'untar',
    description: '解压tar压缩包',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'unzip',
    description: '解压zip压缩包',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'unrar',
    description: '解压rar压缩包',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'un7z',
    description: '解压7z压缩包',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'md5',
    description: '计算文件md5值',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'sha1',
    description: '计算文件sha1值',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'sha256',
    description: '计算文件sha256值',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'sha512',
    description: '计算文件sha512值',
    args: {name: 'files', description: '多个文件', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'diff',
    description: '对比两个文件夹差异',
    args: [
      {name: 'folder', description: '文件夹', template: 'folders'},
      {name: 'folder', description: '文件夹', template: 'folders'},
    ]
  }, {
    name: 'http',
    description: '在当前路径下开启多线程http服务',
    args: [
      {name: 'IP', description: '地址', isOptional: true},
      {name: 'port', description: '端口', isOptional: true},
    ]
  }, {
    name: 'netinfo',
    description: '获取命令参数或剪切板中链接或ip的信息',
    args: {name: 'IPs', description: '多个地址', isOptional: true, isVariadic: true}
  }, {
    name: 'dl',
    description: '从命令参数或剪切板中链接下载文件',
    args: {name: 'urls', description: '多个链接', isOptional: true, isVariadic: true},
    options: [
      {name: '--name', description: '文件名'},
      {name: ['-v', '--video'], description: '使用youtube-dl下载视频'},
      {name: ['-px', '--proxy'], description: '使用配置表中的默认代理下载'}
    ]
  }, {
    name: 'wifi',
    description: '连接WiFi'
  }, {
    name: 'upload',
    description: '上传你的pypi仓库'
  }, {
    name: 'upgrade',
    description: '更新qs'
  }, {
    name: 'trans',
    description: '翻译命令参数或剪切板中的内容',
    args: {name: 'content', description: '待翻译的内容', isVariadic: true, isOptional: true}
  }, {
    name: 'pinyin',
    description: '获取中文内容的拼音',
    args: {name: 'content', description: '内容', isVariadic: true, isOptional: true}
  }, {
    name: 'rmbg',
    description: '移除图片背景',
    args: {name: 'image', description: '图像文件', template: 'filepaths'}
  }, {
    name: 'smms',
    description: '将图片或Markdown中图片上传至sm.ms',
    args: {name: 'file', description: '图像文件或Markdown文件', template: 'filepaths'}
  }, {
    name: 'upimg',
    description: '将图片或Markdown中图片上传至多平台',
    args: [
      {name: 'file', description: '图像文件或Markdown文件', template: 'filepaths'},
      {name: 'platform', description: '平台', isOptional: true}
    ],
    options: [
      {name: ['-h', '--help'], description: '帮助'}
    ]
  }, {
    name: 'alioss',
    description: '阿里云对象存储',
    options: [
      {name: '--help', description: '帮助'},
      {name: '-up', description: '上传文件', args: {name: 'file', description: '文件', template: 'filepaths'}},
      {name: '-rm', description: '删除文件', args: {name: 'file', description: '文件', isDangerous: true}},
      {name: '-dl', description: '下载文件', args: {name: 'file', description: '文件'}},
      {name: '-ls', description: '查看所有文件'}
    ]
  }, {
    name: 'txcos',
    description: '腾讯云对象存储',
    options: [
      {name: '--help', description: '帮助'},
      {name: '-up', description: '上传文件', args: {name: 'file', description: '文件', template: 'filepaths'}},
      {name: '-rm', description: '删除文件', args: {name: 'file', description: '文件', isDangerous: true}},
      {name: '-dl', description: '下载文件', args: {name: 'file', description: '文件'}},
      {name: '-ls', description: '查看所有文件'}
    ]
  }, {
    name: 'qiniu',
    description: '七牛对象存储',
    options: [
      {name: '--help', description: '帮助'},
      {name: '-up', description: '上传文件', args: {name: 'file', description: '文件', template: 'filepaths'}},
      {name: '-rm', description: '删除文件', args: {name: 'file', description: '文件', isDangerous: true}},
      {name: '-dl', description: '下载文件', args: {name: 'file', description: '文件'}},
      {name: '-cp', description: '拷贝文件', args: {name: 'url', description: '链接'}},
      {name: '-ls', description: '查看所有文件'}
    ]
  }, {
    name: 'weather',
    description: '获取当地天气 (或指定地址天气)',
    args: {name: 'address', description: '城市拼音', isOptional: true}
  }, {
    name: 'LG',
    description: '通过百度图像效果增强放大图片',
    args: {name: 'image', description: '图像文件', template: 'filepaths'}
  }, {
    name: 'nlp',
    description: '通过百度NLP进行文本纠错',
    args: {name: 'content', description: '待翻译的内容', isVariadic: true, isOptional: true}
  }, {
    name: 'bcv',
    description: '获取B站视频、直播封面图片',
    args: {name: 'url, code', description: '链接或视频号'}
  }, {
    name: 'gbc',
    description: '查询垃圾分类',
    args: {name: 'garbage', description: '垃圾名称', isVariadic: true}
  }, {
    name: 'svi',
    description: '获取多平台短视频信息 (展示链接)',
    args: {name: 'url', description: '链接或粘贴板内链接', isOptional: true}
  }, {
    name: 'svd',
    description: '下载多平台短视频为mp4',
    args: {name: 'url', description: '链接或粘贴板内链接', isOptional: true}
  }, {
    name: 'acg',
    description: '获取一张acg图片链接 (或保存图片)',
    options: [
      {name: '--save', description: '保存图片'}
    ]
  }, {
    name: 'bing',
    description: '获取一张bing图片链接 (或保存图片)',
    options: [
      {name: '--save', description: '保存图片'}
    ]
  }, {
    name: 'phi',
    description: '获取一张bing图片链接 (或保存图片)',
    args: {name: 'url', description: '链接'},
    options: [
      {name: '--save', description: '保存图片'}
    ]
  }, {
    name: 'loli',
    description: '获取一张萝莉图片链接 [或(使用默认代理)下载]',
    options: [
      {name: '-p', description: '使用默认代理下载'},
      {name: '--save', description: '保存图片'}
    ]
  }, {
    name: 'setu',
    description: '随机调用acg, acg2, loli',
    options: [
      {name: '-p', description: '使用默认代理下载'},
      {name: '--save', description: '保存图片'}
    ]
  }, {
    name: 'kd',
    description: '查询国内快递',
    args: {name: 'CN', description: '快递单号'}
  }, {
    name: 'exc',
    description: '汇率查询<number> <to> 对应 多少 <fr>',
    args: [
      {name: 'number', description: '数量'},
      {name: 'to', description: '待查询币种'},
      {name: 'fr', description: '目标币种 (或默认币种)', isOptional: true}
    ]
  }, {
    name: 'zhihu',
    description: '获取知乎日报'
  }, {
    name: 'wallhaven',
    description: '获取Wallhaven Top动漫涩图',
    options: [
      {name: '--save', description: '保存图片'},
      {name: '-h', description: '帮助'},
      {name: '-one', description: '随机一张'},
      {name: '--url', description: '设置爬取默认页面', args: {name: 'url', description: '链接'}},
    ]
  }, {
    name: 'lmgtfy',
    description: '获取关键词的LMGTFY链接',
    args: {name: 'keyword', description: '关键词'}
  }, {
    name: 'd60',
    description: '获取每日60秒早报',
    options: [
      {name: '--save', description: '保存壁纸'}
    ]
  }, {
    name: 'm2t',
    description: '转换磁力链接为种子文件',
    args: {name: 'magnet', description: '磁力链接 (默认从粘贴板中获取)', isOptional: true},
    options: [
      {name: '-u', description: '设置magnet链接', args: {name: 'magnet', description: '磁力链接'}},
      {name: '-f', description: '读取文件中的magnet链接', args: {name: 'file', description: '文件', template: 'filepaths'}}
    ]
  }, {
    name: 'd2m',
    description: '搜索番号的磁力链',
    args: {name: 'designation', description: '番号'}
  }, {
    name: 'doutu',
    description: '斗图',
    args: {name: 'keyword', description: '关键词'}
  }, {
    name: 'stbg',
    description: '替换图片颜色',
    args: [
      {name: 'image', description: '图片', template: 'filepaths'},
      {name: 'to', description: '十六进制或RGB颜色'},
      {name: 'from', description: '十六进制或RGB颜色, 默认透明', isOptional: true}
    ]
  }, {
    name: 'icat',
    description: '在终端预览图片(仅支持Mac iTerm2)',
    args: {name: 'image', description: '图片', template: 'filepaths'}
  }, {
    name: 'v2gif',
    description: '将视频导出为gif',
    args: [
      {name: 'video', description: '视频', template: 'filepaths'},
      {name: 'sz', description: '尺寸(","分隔)', isOptional: true},
      {name: 'fps', description: '帧率', isOptional: true}
    ]
  }, {
    name: 'v2mp4',
    description: '将视频导出为mp4',
    args: {name: 'video', description: '视频', template: 'filepaths'}
  }, {
    name: 'v2mp3',
    description: '提取视频音频为mp3',
    args: {name: 'video', description: '视频', template: 'filepaths'}
  }, {
    name: 'rmaudio',
    description: '删除mp4文件音频',
    args: {name: 'video', description: '视频', template: 'filepaths'}
  }, {
    name: 'i2png',
    description: '将图像转换为png',
    args: {name: 'image', description: '图片', isVariadic: true, template: 'filepaths'}
  }, {
    name: 'i2jpg',
    description: '将图像转换为jpg',
    args: {name: 'image', description: '图片', isVariadic: true, template: 'filepaths'}
  }, {
    name: 'fmti',
    description: '格式化图片颜色为<to>, 忽略[exp...]颜色',
    args: [
      {name: 'image', description: '图片', template: 'filepaths'},
      {name: 'to', description: '十六进制或RGB颜色'},
      {name: 'exp', description: '忽略的十六进制或RGB颜色', isVariadic: true}
    ]
  }, {
    name: 'vsta',
    description: '设置视频的音频',
    args: [
      {name: 'video', description: '视频', template: 'filepaths'},
      {name: 'audio', description: '音频', template: 'filepaths'}
    ]
  }],
};
export default completionSpec;
