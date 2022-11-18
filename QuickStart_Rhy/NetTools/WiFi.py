# coding=utf-8
"""
qs的WIFI模块, 协助连接WIFI, 但不支持机构WIFI自动登录

The WiFi module of QS helps to connect WiFi, but does not support the automatic login of institutional WiFi
"""
import time
from .. import user_lang, qs_default_console, qs_error_string, requirePackage

const = requirePackage("pywifi", "const")
PyWiFi = requirePackage("pywifi", "PyWiFi")


class WiFi:
    def __init__(self) -> None:
        """
        qs的wifi工具 (Windows 或 Linux)
        """
        self.wifi_engine = PyWiFi()
        self.ifaces = self.wifi_engine.interfaces()
        self.iface = self.ifaces[0]

    def status(self) -> str:
        """
        判断当前wifi连接状态

        Determine the current wifi connection status

        :return: 连接的wifi名 | The name of the connecting wifi
        """
        flag = self.iface.status() in [const.IFACE_CONNECTED, const.IFACE_CONNECTING]
        return self.iface.name if flag else ""

    def scan(self):
        """
        扫描附近可连接的wifi

        Scan for nearby wifi connections

        :return: 按信号强度排序好的可连接wifi列表 | A list of available wifi connections sorted by signal strength
        """
        self.iface.scan()
        time.sleep(1)
        res = self.iface.scan_results()
        wifi_ls = []
        for i in res:
            if i not in wifi_ls and i.signal > -90:
                wifi_ls.append((i.ssid, i.signal, i.akm))
        return sorted(wifi_ls, key=lambda x: x[1], reverse=True)

    def set_iface(self):
        """
        设置网卡接口

        Set Network port

        :return: None
        """
        num = len(self.ifaces)
        if num <= 0:
            qs_default_console.log(
                qs_error_string,
                "There is no recognizable network card interface"
                if user_lang != "zh"
                else "没有可识别的网卡接口",
            )
            return
        elif num != 1:
            from ..TuiTools.Table import qs_default_table

            table = qs_default_table(
                ["id", "interface"] if user_lang != "zh" else ["序号", "网卡"]
            )
            for i, w in enumerate(self.ifaces):
                table.add_row(str(i), w.name())
            qs_default_console.print(table)
            while True:
                iface_no = input(
                    "请选择网卡接口序号: " if user_lang != "zh" else "Select interface by id: "
                )
                try:
                    no = int(iface_no)
                    if 0 <= no < num:
                        self.iface = self.ifaces[no]
                        break
                except:
                    continue
        else:
            qs_default_console.print(
                f"{'Only one' if user_lang != 'zh' else '仅有可用'}: {self.iface.name()}"
            )

    def conn(self, ssid, password):
        """
        连接WiFi

        connect WiFi

        :param ssid: wifi名称
        :param password: 密码
        :return: status
        """
        # from pywifi import Profile
        Profile = requirePackage("pywifi", "Profile")
        self.iface.disconnect()
        time.sleep(1)
        pinfo = Profile()
        pinfo.ssid = ssid
        pinfo.auth = const.AUTH_ALG_OPEN
        pinfo.akm.append(const.AKM_TYPE_WPA2PSK)
        pinfo.cipher = const.CIPHER_TYPE_CCMP
        pinfo.key = password
        self.iface.remove_all_network_profile(pinfo)
        tmp = self.iface.add_network_profile(pinfo)
        self.iface.connect(tmp)
        time.sleep(5)
        return self.status()

    def disconn(self):
        """
        断开wifi连接

        disconnect wifi
        :return: status
        """
        self.iface.disconnect()
        return self.status()
