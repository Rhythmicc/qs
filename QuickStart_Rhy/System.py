# coding=utf-8
"""
调用各种系统工具

Call various system tools
"""
import QuickStart_Rhy.Wrapper as _wrapper

miss_file = [".DS_Store"]


def __latest_filename(name):
    import os

    cur = os.getcwd()
    while cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, name)):
            return os.path.join(cur, name)
        cur = os.path.dirname(cur)
    return os.path.join(cur, name) if os.path.exists(os.path.join(cur, name)) else ""


def top():
    """
    CPU和内存监测

    CPU and memory monitoring

    :return: None
    """
    import sys

    sys.argv = ["bpytop"] + sys.argv[2:]

    from . import requirePackage

    requirePackage("bpytop", "main")()


def clear_mem():
    """
    清理系统内存

    Clean system memory

    :return: None
    """
    from .SystemTools import clear_mem

    clear_mem()


def go_github():
    """
    自动识别当前文件夹.git/config中的地址，并通过浏览器打开

    Automatically recognize the address in the current folder .git/config and open it through a browser
    """
    import os
    from . import (
        qs_default_console,
        qs_error_string,
        user_lang,
        open_url,
        requirePackage,
    )

    config_path = __latest_filename(".git/config")
    if not os.path.exists(config_path):
        qs_default_console.print(
            qs_error_string,
            "No a git dictionary" if user_lang != "zh" else "不是 git 文件夹",
        )
        return
    config = requirePackage("configparser", "ConfigParser")()
    config.read(filenames=config_path)
    url_ls = []
    for section in config.sections():
        if section.startswith("remote"):
            url_ls.append(config[section]["url"].replace(".git", ""))
    open_url(url_ls)


def mktar():
    """
    创建tar包

    Create a tar packages

    :return: None
    """

    @_wrapper.mkCompressPackageWrap
    def _mktar(file_path: str = ""):
        from .SystemTools.Compress import Tar

        return Tar(file_path + ".tar.gz", "w")

    return _mktar()


def untar():
    """
    解压tar包

    Unpack the tar packages

    :return: None
    """

    @_wrapper.unCompressPackageWrap
    def _untar(file_path: str = ""):
        from .SystemTools.Compress import Tar

        return Tar(file_path)

    return _untar()


def mkzip():
    """
    创建ZIP包

    Create a ZIP package

    :return: None
    """

    @_wrapper.mkCompressPackageWrap
    def _mkzip(file_path: str = ""):
        from .SystemTools.Compress import Zip

        return Zip(file_path + ".zip", "w")

    return _mkzip()


def unzip():
    """
    解压ZIP包

    Unpack the ZIP package

    :return: None
    """

    @_wrapper.unCompressPackageWrap
    def _unzip(file_path: str = ""):
        from .SystemTools.Compress import Zip

        return Zip(file_path, "r")

    return _unzip()


def unrar():
    """
    解压RAR包

    Extract RAR package

    :return: None
    """

    @_wrapper.unCompressPackageWrap
    def _unrar(file_path: str = ""):
        from .SystemTools.Compress import Rar

        return Rar(file_path)

    return _unrar()


def mk7z():
    """
    创建7z包

    Create 7z package

    :return: None
    """

    @_wrapper.mkCompressPackageWrap
    def _mk7z(file_path: str = ""):
        from .SystemTools.Compress import SevenZip

        return SevenZip(file_path + ".7z", "w")

    return _mk7z()


def un7z():
    """
    解压7z包

    Extract 7z package

    :return:
    """

    @_wrapper.unCompressPackageWrap
    def _un7z(file_path: str = ""):
        from .SystemTools.Compress import SevenZip

        return SevenZip(file_path)

    return _un7z()


@_wrapper.HashWrapper()
def md5():
    """
    获取文件md5值
    :return:
    """


@_wrapper.HashWrapper()
def sha1():
    """
    获取文件sha1值
    :return:
    """


@_wrapper.HashWrapper()
def sha256():
    """
    获取文件sha256值
    :return:
    """


@_wrapper.HashWrapper()
def sha512():
    """
    获取文件sha512值
    :return:
    """


def diff_dir():
    """
    对比两个文件夹差异，并生成相应html对比结果
    :return:
    """
    from . import user_lang, qs_default_console, qs_info_string, qs_default_status
    from .SystemTools.Diff import DictionaryFiles
    import sys

    if "-h" in sys.argv:
        qs_default_console.print(
            qs_info_string, "Usage: qs diff <dir1> <dir2> [-x <name or regex pattern>]"
        )

    d1, d2 = sys.argv[2:4]
    apply_ignore = sys.argv[sys.argv.index("-x") + 1 :] if "-x" in sys.argv else None
    d1 = DictionaryFiles(d1, apply_ignore)
    d2 = DictionaryFiles(d2, apply_ignore)

    if not (d1.available and d2.available):
        return

    with qs_default_status(
        "Generating diff result.." if user_lang != "zh" else "生成对比结果中.."
    ):
        from .SystemTools.Diff import DiffFilesToStructHtml

        DiffFilesToStructHtml(d1, d2).generate()


def mount_dmg():
    """
    挂载镜像

    :return:
    """
    from .SystemTools.DiskMac import DMG
    import sys

    DMG().mount(sys.argv[2])


def unmount_dmg():
    """
    卸载镜像
    """
    from .SystemTools.DiskMac import DMG
    from .TuiTools.Table import qs_default_table
    from . import qs_default_console, user_lang, qs_info_string, _ask

    disks = DMG()
    _ls = disks.get_disk_list()[2:]
    if not _ls:
        return qs_default_console.print(
            qs_info_string, "No DMG disk found" if user_lang != "zh" else "没有找到 dmg 磁盘"
        )
    table = qs_default_table(["Disk", "Type", "Size"])
    for disk in _ls:
        table.add_row(disk["path"], disk["type"], disk["size"])
    qs_default_console.print(table, justify="center")
    disk_path = _ask(
        {
            "type": "list",
            "message": "Select a disk to umount" if user_lang != "zh" else "选择要卸载的磁盘",
            "choices": [disk["path"] for disk in _ls],
            "default": _ls[0]["path"],
        }
    )
    disks.unmount(disk_path)
