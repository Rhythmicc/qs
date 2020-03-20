import sys
from QuickStart_Rhy.basic import dir_char
from QuickStart_Rhy.func_list import *

color_flag = dir_char == '\\'


def help():
    import colorama

    def color_rep(ss):
        global color_flag
        if color_flag:
            colorama.init()
            color_flag = False
        ss = ss.split(':->')
        return colorama.Fore.LIGHTMAGENTA_EX + ss[0] + colorama.Style.RESET_ALL + \
               ':->' + colorama.Fore.YELLOW + ss[1] + colorama.Style.RESET_ALL

    print('help:')
    print(color_rep('    qs -u  <url>             :-> open url using default browser'))
    print(color_rep('    qs -a  <app> [file..]    :-> open app or open file by app(for Mac OS X)'))
    print(color_rep('    qs -f  <file...>         :-> open file by default app'))
    print(color_rep('    qs -dl [urls]            :-> download file from url(in clipboard)'))
    print(color_rep('    qs -trans [content]      :-> translate the content(in clipboard)'))
    print(color_rep('    qs -time                 :-> view current time'))
    print(color_rep('    qs -ftp                  :-> start a simple ftp server'))
    print(color_rep('    qs -top                  :-> cpu and memory monitor'))
    print(color_rep('    qs -rmbg <picture>       :-> remove image background'))
    print(color_rep('    qs -stbg pic to [from]   :-> color replace for picture'))
    print(color_rep('    qs -smms <picture/*.md>  :-> upload img to smms or all in .md'))
    print(color_rep('    qs -ali_oss -help        :-> get aliyun nas api help menu'))
    print(color_rep('    qs -qiniu -help          :-> get qiniu nas api help menu'))
    print(color_rep('    qs -weather [address]    :-> check weather (of address)'))
    print(color_rep('    qs -mktar <path...>      :-> create gzipped archive for path'))
    print(color_rep('    qs -untar <path>         :-> extract path.tar.*'))
    print(color_rep('    qs -mkzip <path...>      :-> make a zip for path'))
    print(color_rep('    qs -unzip <path>         :-> unzip path.zip'))
    print(color_rep('    qs -upload               :-> upload your pypi library'))
    print(color_rep('    qs -upgrade              :-> update qs'))


cmd_config = {}
for i in basic_funcs:
    cmd_config[i] = basic_funcs
for i in api_funcs:
    cmd_config[i] = api_funcs
for i in net_funcs:
    cmd_config[i] = net_funcs
for i in image_funcs:
    cmd_config[i] = image_funcs
for i in system_funcs:
    cmd_config[i] = system_funcs


def main():
    if len(sys.argv) >= 2:
        func_name = sys.argv[1]
        if func_name not in cmd_config:
            help()
        else:
            func_table = cmd_config[func_name]
            file_name = func_table['self']
            func_name = func_table[func_name]
            exec('from QuickStart_Rhy.%s import %s' % (file_name, func_name))
            eval('%s()' % func_name)
    else:
        help()


if __name__ == '__main__':
    main()
