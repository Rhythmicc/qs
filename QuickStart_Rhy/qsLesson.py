# coding=utf-8
"""
命令交互，查看qs的各种菜单和文档

Command interaction, view various menus and documents of QS
"""
from . import user_lang, open_url
from .__config__ import prompt


def onlineDocuments():
    res = prompt({
        'type': 'list',
        'name': 'onlineSource',
        'message': 'Switch a website source:' if user_lang != 'zh' else '选择合适你的网站源:',
        'choices': [
            '1. CDN in China' if user_lang != 'zh' else '1. 国内CDN',
            '2. Github Page (non-Chinese users)' if user_lang != 'zh' else '2. Github Page (非中国用户)',
        ]
    })['onlineSource']
    import webbrowser as wb
    wb.open(
        {
            '1': 'https://rhythmlian.cn/' + ('2020/02/14/QuickStart-Rhy/'
                                             if user_lang != 'zh' else '2020/08/09/QuickStart-Rhy-zh/'),
            '2': 'https://rhythmicc.github.io/' + ('2020/02/14/QuickStart-Rhy/'
                                                   if user_lang != 'zh' else '2020/08/09/QuickStart-Rhy-zh/'),
        }[res[0]]
    )


def lesson():
    mainMenu = {
        'type': 'list',
        'name': 'action',
        'message': 'Welcome using qs, choose and get help:' if user_lang != 'zh' else '欢迎使用qs, 选择以下选项获得帮助:',
        'choices': [
            '1. basic tools' if user_lang != 'zh' else '1. 基础工具',
            '2. system tools' if user_lang != 'zh' else '2. 系统工具',
            '3. network tools' if user_lang != 'zh' else '3. 网路工具',
            '4. api tools' if user_lang != 'zh' else '4. 扩展工具',
            '5. image tools' if user_lang != 'zh' else '5. 图像工具',
            '6. online Docs' if user_lang != 'zh' else '6. 在线文档',
            '7. join TG group' if user_lang != 'zh' else '7. 加入TG群'
        ]
    }
    res = prompt(mainMenu)['action']

    if res[0] == '7':
        return open_url(['https://t.me/joinchat/G2mpk7-S85eM7sb7'])
    else:
        from .funcList import menu_table
        {
            '1': menu_table['basic'],
            '2': menu_table['system'],
            '3': menu_table['net'],
            '4': menu_table['api'],
            '5': menu_table['image'],
            '6': onlineDocuments,
        }[res[0]]()
