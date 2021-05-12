# coding=utf-8
"""
调用各种系统工具

Call various system tools
"""
import QuickStart_Rhy.Wrapper as _wrapper

miss_file = ['.DS_Store']


def top():
    """
    CPU和内存监测

    CPU and memory monitoring

    :return: None
    """
    from . import dir_char
    if dir_char == '\\':
        from .SystemTools.Monitor import top
        top()
    else:
        import sys
        sys.argv = ['bpytop'] + sys.argv[2:]

        from . import requirePackage
        requirePackage('bpytop', 'main')()


def clear_mem():
    """
    清理系统内存

    Clean system memory

    :return: None
    """
    from .SystemTools import clear_mem
    clear_mem()


@_wrapper.mkCompressPackageWrap
def _mktar(filePath: str = ''):
    from .SystemTools.Compress import Tar
    return Tar(filePath + '.tar.gz', 'w')


def mktar():
    """
    创建tar包

    Create a tar packages

    :return: None
    """
    return _mktar()


@_wrapper.unCompressPackageWrap
def _untar(filePath: str = ''):
    from .SystemTools.Compress import Tar
    return Tar(filePath)


def untar():
    """
    解压tar包

    Unpack the tar packages

    :return: None
    """
    return _untar()


@_wrapper.mkCompressPackageWrap
def _mkzip(filePath: str = ''):
    from .SystemTools.Compress import Zip
    return Zip(filePath + '.zip', 'w')


def mkzip():
    """
    创建ZIP包

    Create a ZIP package

    :return: None
    """
    return _mkzip()


@_wrapper.unCompressPackageWrap
def _unzip(filePath: str = ''):
    from .SystemTools.Compress import Zip
    return Zip(filePath, 'r')


def unzip():
    """
    解压ZIP包

    Unpack the ZIP package

    :return: None
    """
    return _unzip()


@_wrapper.unCompressPackageWrap
def _unrar(filePath: str = ''):
    from .SystemTools.Compress import Rar
    return Rar(filePath)


def unrar():
    """
    解压RAR包

    Extract RAR package

    :return: None
    """
    return _unrar()


@_wrapper.mkCompressPackageWrap
def _mk7z(filePath: str = ''):
    from .SystemTools.Compress import SevenZip
    return SevenZip(filePath + '.7z', 'w')


def mk7z():
    """
    创建7z包

    Create 7z package

    :return: None
    """
    return _mk7z()


@_wrapper.unCompressPackageWrap
def _un7z(filePath: str = ''):
    from .SystemTools.Compress import SevenZip
    return SevenZip(filePath)


def un7z():
    """
    解压7z包

    Extract 7z package

    :return:
    """
    return _un7z()


@_wrapper.HashWrapper('md5')
def md5():
    """
    获取文件md5值
    :return:
    """


@_wrapper.HashWrapper('sha1')
def sha1():
    """
    获取文件sha1值
    :return:
    """


@_wrapper.HashWrapper('sha256')
def sha256():
    """
    获取文件sha256值
    :return:
    """


@_wrapper.HashWrapper('sha512')
def sha512():
    """
    获取文件sha512值
    :return:
    """


def diffDir():
    """
    对比两个文件夹差异，并生成相应html对比结果
    :return:
    """
    from . import user_lang, qs_default_console, qs_info_string
    from .SystemTools.Diff import DictionaryFiles
    import sys

    if '-h' in sys.argv:
        qs_default_console.print(qs_info_string, 'Usage: qs diff <dir1> <dir2> [-x <name or regex pattern>]')

    d1, d2 = sys.argv[2:4]
    applyIgnore = sys.argv[sys.argv.index('-x') + 1:] if '-x' in sys.argv else None
    d1 = DictionaryFiles(d1, applyIgnore)
    d2 = DictionaryFiles(d2, applyIgnore)

    if not (d1.available and d2.available):
        return

    with qs_default_console.status('Generating diff result..' if user_lang != 'zh' else '生成对比结果中..') as st:
        from .SystemTools.Diff import DiffFilesToStructHtml

        DiffFilesToStructHtml(d1, d2).generate()
