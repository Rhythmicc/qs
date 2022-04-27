export const generateApps = (unquotedPath: string): Fig.Generator => ({
  cache: { strategy: "stale-while-revalidate" },
  script: `mdfind kMDItemContentTypeTree=com.apple.application-bundle -onlyin ${unquotedPath}`,
  postProcess: (out) => {
    return out.split("\n").map((path) => {
      const basename = path.slice(path.lastIndexOf("/") + 1);
      return {
        name: basename,
        description: path,
        icon: `fig://${path}`,
        priority: path.endsWith(`/Applications/${basename}`)
          ? 80
          : path.startsWith("/Applications")
          ? 76
          : 50,
      };
    });
  },
});

const completionSpec: Fig.Spec = {
  name: "qs",
  description: "QuickStart_Rhy--Your command line assistant",
  subcommands: [{
    name: 'basic',
    description: 'basic tools help',
  }, {
    name: 'system',
    description: "system tools help",
  }, {
    name: 'net',
    description: 'network tools help',
  }, {
    name: 'api',
    description: 'api tools help',
  }, {
    name: 'image',
    description: 'image tools help',
  }, {
    name: 'u',
    description: 'open urls using default browser',
    args: {name: 'url', description: 'URL', isVariadic: true}
  }, {
    name: 'a',
    description: 'open app or open file by app(for Mac OS)',
    args: [
        {name: 'app', description: 'app', generators: generateApps('/')},
        {name: 'files', description: 'files', isOptional: true, isVariadic: true, template: ['filepaths','folders']}
    ]
  }, {
    name: 'f',
    description: 'open file by default app',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'cal',
    description: 'calculate exp',
    args: {name: 'exp', description: 'expression'}
  }, {
    name: 'time',
    description: 'view current time'
  }, {
    name: 'pcat',
    description: 'output string in clipboard'
  }, {
    name: 'fcopy',
    description: 'copy file content to clipboard',
    args: {name: 'file', description: 'file', template: ['filepaths', 'folders']}
  }, {
    name: 'play',
    description: 'play audio file',
    args: {name: 'music', description: '音乐', template: ['filepaths', 'folders'], isVariadic: true}
  }, {
    name: 'top',
    description: 'cpu and memory monitor',
  }, {
    name: 'clear',
    description: 'free memory',
    isDangerous:  true
  }, {
    name: 'go2git',
    description: 'go to the webpage of the git config'
  }, {
    name: 'mktar',
    description: 'create gzipped archive for path',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'mkzip',
    description: 'make a zip for path',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'mk7z',
    description: 'make a 7z archive for path',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'untar',
    description: 'extract *.tar.*',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'unzip',
    description: 'extract *.zip file',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'unrar',
    description: 'extract *.rar file',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'un7z',
    description: 'extract *.7z file',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths', 'folders']}
  }, {
    name: 'md5',
    description: 'calculate md5 of files',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'sha1',
    description: 'calculate SHA1 of files',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'sha256',
    description: 'calculate SHA256 of files',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'sha512',
    description: 'calculate SHA512 of files',
    args: {name: 'files', description: 'files', isVariadic: true, template: ['filepaths']}
  }, {
    name: 'diff',
    description: 'diff two directories',
    args: [
      {name: 'folder', description: 'folder', template: 'folders'},
      {name: 'folder', description: 'folder', template: 'folders'},
    ]
  }, {
    name: 'http',
    description: 'start a multi thread ftp server',
    args: [
      {name: 'IP', description: 'IP', isOptional: true},
      {name: 'port', description: 'port', isOptional: true},
    ]
  }, {
    name: 'netinfo',
    description: 'get url\'s info which in clipboard or params',
    args: {name: 'urls', description: 'urls', isOptional: true, isVariadic: true}
  }, {
    name: 'dl',
    description: 'download file from url(in clipboard)',
    args: {name: 'urls', description: 'urls', isOptional: true, isVariadic: true},
    options: [
      {name: '--name', description: 'filename'},
      {name: ['-v', '--video'], description: 'download video (use youtube-dl)'},
      {name: ['-px', '--proxy'], description: 'use default proxy set in ~/.qsrc'}
    ]
  }, {
    name: 'wifi',
    description: 'connect wifi'
  }, {
    name: 'upload',
    description: 'upload your pypi library'
  }, {
    name: 'upgrade',
    description: 'update qs'
  }, {
    name: 'pinyin',
    description: 'get the pinyin of Chinese content',
    args: {name: 'content', description: 'content', isVariadic: true, isOptional: true}
  }, {
    name: 'rmbg',
    description: 'remove image background',
    args: {name: 'image', description: 'image', template: 'filepaths'}
  }, {
    name: 'smms',
    description: 'upload img or img in markdown to sm.ms',
    args: {name: 'file', description: 'image or markdown file', template: 'filepaths'}
  }, {
    name: 'upimg',
    description: 'upload img or img in markdown to platform',
    args: [
      {name: 'file', description: 'image or markdown file', template: 'filepaths'},
      {name: 'platform', description: 'platform', isOptional: true}
    ],
    options: [
      {name: ['-h', '--help'], description: 'help'}
    ]
  }, {
    name: 'alioss',
    description: 'aliyun oss api',
    options: [
      {name: '--help', description: 'help'},
      {name: '-up', description: 'upload file', args: {name: 'file', description: 'file', template: 'filepaths'}},
      {name: '-rm', description: 'remove file', args: {name: 'file', description: 'file', isDangerous: true}},
      {name: '-dl', description: 'download file', args: {name: 'file', description: 'file'}},
      {name: '-ls', description: 'list all files'}
    ]
  }, {
    name: 'txcos',
    description: 'tencent cos api',
    options: [
      {name: '--help', description: 'help'},
      {name: '-up', description: 'upload file', args: {name: 'file', description: 'file', template: 'filepaths'}},
      {name: '-rm', description: 'remove file', args: {name: 'file', description: 'file', isDangerous: true}},
      {name: '-dl', description: 'download file', args: {name: 'file', description: 'file'}},
      {name: '-ls', description: 'list all files'}
    ]
  }, {
    name: 'qiniu',
    description: 'qiniu oss api',
    options: [
      {name: '--help', description: 'help'},
      {name: '-up', description: 'upload file', args: {name: 'file', description: 'file', template: 'filepaths'}},
      {name: '-rm', description: 'remove file', args: {name: 'file', description: 'file', isDangerous: true}},
      {name: '-dl', description: 'download file', args: {name: 'file', description: 'file'}},
      {name: '-cp', description: 'copy file', args: {name: 'url', description: 'url'}},
      {name: '-ls', description: 'list all files'}
    ]
  }, {
    name: 'weather',
    description: 'check weather (of address)',
    args: {name: 'address', description: 'city', isOptional: true}
  }, {
    name: 'LG',
    description: 'make image larger(with AI)',
    args: {name: 'image', description: 'image', template: 'filepaths'}
  }, {
    name: 'nlp',
    description: 'Text(or in clipboard) error correction',
    args: {name: 'content', description: 'content', isVariadic: true, isOptional: true}
  }, {
    name: 'bcv',
    description: 'get Bilibili video cover image with <url>',
    args: {name: 'url, code', description: 'url or video code'}
  }, {
    name: 'gbc',
    description: 'check Chinese garbage classification',
    args: {name: 'garbage', description: 'garbage', isVariadic: true}
  }, {
    name: 'svi',
    description: 'get short video info (show url)',
    args: {name: 'url', description: 'url (or in clipboard)', isOptional: true}
  }, {
    name: 'svd',
    description: 'download short video info as mp4',
    args: {name: 'url', description: 'url (or in clipboard)', isOptional: true}
  }, {
    name: 'acg',
    description: 'get an acg image link (or save)',
    options: [
      {name: '--save', description: 'save image'}
    ]
  }, {
    name: 'bing',
    description: 'get an bing image link ( or save image)',
    options: [
      {name: '--save', description: 'save image'}
    ]
  }, {
    name: 'phi',
    description: 'get <image url> in url (preview on Mac)',
    args: {name: 'url', description: 'url'},
    options: [
      {name: '--save', description: 'save image'}
    ]
  }, {
    name: 'loli',
    description: 'get and loli image link [or save (use default proxy)]',
    options: [
      {name: '-p', description: 'use default proxy'},
      {name: '--save', description: 'save image'}
    ]
  }, {
    name: 'setu',
    description: 'randomly call acg, acg2, loli',
    options: [
      {name: '-p', description: 'use default proxy'},
      {name: '--save', description: 'save image'}
    ]
  }, {
    name: 'kd',
    description: 'Query China express',
    args: {name: 'CN', description: 'courier number'}
  }, {
    name: 'exc',
    description: 'Query <number> <to> corresponding <number?> <fr>',
    args: [
      {name: 'number', description: 'number'},
      {name: 'to', description: 'query currency'},
      {name: 'fr', description: 'aim currency (or default currency)', isOptional: true}
    ]
  }, {
    name: 'zhihu',
    description: 'Get zhihu.com Daily'
  }, {
    name: 'wallhaven',
    description: 'Get Wallhaven Toplist',
    options: [
      {name: '--save', description: 'save image'}
    ]
  }, {
    name: 'lmgtfy',
    description: 'Get LMGTFY link for keywords',
    args: {name: 'keyword', description: 'keyword'}
  }, {
    name: 'd60',
    description: 'Get the daily 60-second morning report',
    options: [
      {name: '--save', description: 'save post'}
    ]
  }, {
    name: 'm2t',
    description: 'transform magnet link to torrent file',
    args: {name: 'magnet', description: 'magnet url (in clipboard)', isOptional: true},
    options: [
      {name: '-u', description: 'set magnet url', args: {name: 'magnet', description: 'magnet url'}},
      {name: '-f', description: 'read magnet url in file', args: {name: 'file', description: 'file', template: 'filepaths'}}
    ]
  }, {
    name: 'd2m',
    description: 'search magnet url by designation',
    args: {name: 'designation', description: 'designation'}
  }, {
    name: 'stbg',
    description: 'color replace for picture',
    args: [
      {name: 'image', description: 'image', template: 'filepaths'},
      {name: 'to', description: 'hex or RGB color'},
      {name: 'from', description: 'hex or RGB color, default transparent', isOptional: true}
    ]
  }, {
    name: 'icat',
    description: 'preview image on terminal (Mac iTerm2 only)',
    args: {name: 'image', description: 'image', template: 'filepaths'}
  }, {
    name: 'v2gif',
    description: 'generate gif from video',
    args: [
      {name: 'video', description: 'video', template: 'filepaths'},
      {name: 'sz', description: 'size (split by ",")', isOptional: true},
      {name: 'fps', description: 'fps', isOptional: true}
    ]
  }, {
    name: 'v2mp4',
    description: 'format video to mp4',
    args: {name: 'video', description: 'video', template: 'filepaths'}
  }, {
    name: 'v2mp3',
    description: 'extract audio from video and save in MP3',
    args: {name: 'video', description: 'video', template: 'filepaths'}
  }, {
    name: 'rmaudio',
    description: 'remove audio in video (return mp4 only)',
    args: {name: 'video', description: 'video', template: 'filepaths'}
  }, {
    name: 'i2png',
    description: 'transform imgs to png',
    args: {name: 'image', description: 'image', isVariadic: true, template: 'filepaths'}
  }, {
    name: 'i2jpg',
    description: 'transform imgs to jpg',
    args: {name: 'image', description: 'image', isVariadic: true, template: 'filepaths'}
  }, {
    name: 'fmti',
    description: 'format image to <to> color except [exp...] color',
    args: [
      {name: 'image', description: 'image', template: 'filepaths'},
      {name: 'to', description: 'hex or RGB color'},
      {name: 'exp', description: 'except hex or RGB color', isVariadic: true}
    ]
  }, {
    name: 'vsta',
    description: 'set video\'s audio',
    args: [
      {name: 'video', description: 'video', template: 'filepaths'},
      {name: 'audio', description: 'audio', template: 'filepaths'}
    ]
  }],
};
export default completionSpec;
