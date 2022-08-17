"""
qs的WIFI模块, 协助连接WIFI, 但不支持机构WIFI自动登录 | 仅在Mac OS下工作

The WiFi module of QS helps to connect WiFi, but does not support the automatic login of institutional WiFi |
(Works only on Mac OS)
"""
import os
import re
from .. import qs_default_console, qs_warning_string, qs_info_string


class WiFi:
    def __init__(self) -> None:
        """
        适用于Mac OS X的wifi工具

        Wifi tools for Mac OS X
        """
        with os.popen('networksetup -listallhardwareports') as pipe:
            ifaces = pipe.read()
        ifaces = [i.split('\n') for i in ifaces.strip().split('\n\n')]
        ifaces.remove(['VLAN Configurations', '==================='])
        self.ifaces = ifaces
        for i in self.ifaces:
            if i[0].endswith('Wi-Fi'):
                self.iface = [j.split()[-1] for j in i[1:]]
                return

    def status(self) -> str:
        """
        判断当前wifi连接状态

        Determine the current wifi connection status

        :return: 连接的wifi名 | The name of the connecting wifi
        """
        with os.popen('networksetup -getairportnetwork %s' % self.iface[0]) as pipe:
            res = pipe.read().strip()
            res = re.sub('.*?:', '', res).strip()
        qs_default_console.print(qs_info_string, f"{'已' if res else '未'}连接", res if res else '')
        return res

    @staticmethod
    def scan():
        """
        扫描附近可连接的wifi

        Scan for nearby wifi connections

        :return: 按信号强度排序好的可连接wifi列表 | A list of available wifi connections sorted by signal strength
        """
        with os.popen(
                '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan') as pipe:
            res = pipe.read().strip().split('\n')[1:]
            tmp_ls = [i.strip().split() for i in res]
            has_add = set()
            res = []
            for i in tmp_ls:
                # mac_index = 0
                # while mac_index < len(i):
                #     if is_mac(i[mac_index]):
                #         break
                #     else:
                #         mac_index += 1
                # if mac_index >= len(i):
                #     qs_default_console.log(qs_warning_string, "Failed to get info with:", i)
                #     continue
                index = i.index('--') - 3
                ssid = ' '.join(i[:index])
                if ssid not in has_add:
                    res.append([ssid, int(i[index]), i[-1]])
                    has_add.add(ssid)
        return sorted(res, key=lambda x: x[1], reverse=True)

    def set_iface(self):
        raise NotImplementedError

    def conn(self, ssid: list, password: str):
        """
        连接WiFi

        connect WiFi

        :param ssid: wifi名称
        :param password: 密码
        :return: status
        """
        from .. import external_exec
        external_exec('networksetup -setairportnetwork %s %s "%s"' % (self.iface[0], ssid[0], password))
        return self.status()

    def disconn(self):
        return NotImplementedError
