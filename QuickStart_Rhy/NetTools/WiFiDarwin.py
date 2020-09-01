import os
import re


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
        print("%s连接" % ('已' if res else '未'), res if res else '')
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
                if i[0] not in has_add:
                    res.append([i[0], int(i[2])])
                    has_add.add(i[0])
        return sorted(res, key=lambda x: x[1], reverse=True)

    def set_iface(self):
        raise NotImplementedError

    def conn(self, ssid, password):
        """
        连接WiFi

        connect WiFi

        :param ssid: wifi名称
        :param password: 密码
        :return: status
        """
        os.system('networksetup -setairportnetwork %s %s %s' % (self.iface[0], ssid, password))
        return self.status()

    def disconn(self):
        return NotImplementedError
