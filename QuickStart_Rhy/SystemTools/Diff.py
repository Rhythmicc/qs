from .. import (
    qs_default_console,
    qs_error_string,
    qs_warning_string,
    user_lang,
    dir_char,
)
from ..SystemTools.FileHash import md5
import os
import re


class DictionaryFiles(set):
    def __init__(self, rt: str, ignorePatterns: list = None):
        """
        :param rt: 目录路径
        """
        super().__init__()
        if ignorePatterns is None:
            ignorePatterns = []
        if not (os.path.exists(rt) or os.path.isdir(rt)):
            qs_default_console.log(
                qs_error_string,
                f'"{rt}" {"Not exist or Not a dictionary!" if user_lang != "zh" else "不存在或不是文件夹"}',
            )
            self.available = False
            return
        self.name = os.path.basename(rt)
        self.rt = os.path.abspath(rt)
        self.available = True
        self.ignored = set(ignorePatterns) if ignorePatterns else None
        self.__getAllPaths()

    def checkIgnore(self, path):
        if self.ignored:
            for item in self.ignored:
                if re.findall(item, path):
                    return True
        return False

    def __getAllPaths(self):
        for rt, sonDir, files in os.walk(self.rt):
            for file in files:
                filePath = os.path.join(rt, file).replace(self.rt, "")
                if self.checkIgnore(filePath):
                    continue
                self.add(filePath)

    def getMd5ByFileItem(self, item: str):
        return md5(self.rt + item)

    def getFilepathByItem(self, item: str):
        return self.rt + item


class DiffFilesToStructHtml:
    from concurrent.futures import ThreadPoolExecutor, wait
    from rich.progress import Progress
    from difflib import HtmlDiff

    def __init__(self, d1: DictionaryFiles, d2: DictionaryFiles):
        self.d1 = d1
        self.d2 = d2
        self.rt = os.path.join(os.getcwd(), d1.name + "-vs-" + d2.name + ".qs_diff")
        self.pool = DiffFilesToStructHtml.ThreadPoolExecutor(max_workers=8)
        self.jobLs = []
        self.progress = DiffFilesToStructHtml.Progress(console=qs_default_console)
        self.pid = self.progress.add_task("compare" if user_lang != "zh" else "对比")

    def _run(self, item: str):
        pathLs = item.strip(dir_char).split(dir_char)[:-1]
        for i in range(len(pathLs)):
            dirName = os.path.join(self.rt, *pathLs[: i + 1])
            if not os.path.exists(dirName):
                os.mkdir(dirName)
        with open(self.d1.getFilepathByItem(item), "r") as f:
            _d1 = f.readlines()
        with open(self.d2.getFilepathByItem(item), "r") as f:
            _d2 = f.readlines()
        _diff = DiffFilesToStructHtml.HtmlDiff().make_file(_d1, _d2)
        with open(self.rt + item + ".html", "w") as f:
            f.write(_diff)
        self.progress.advance(self.pid, 1)

    def generate(self):
        if os.path.exists(self.rt):
            qs_default_console.log(
                qs_warning_string,
                f'"{self.rt}" {"Already exists! QS will delete it and regenerate." if user_lang != "zh" else "已经存在! QS将删除它并重新生成."}',
            )
            from .. import remove

            remove(self.rt)

        os.mkdir(self.rt)
        _tmpLs = []
        for item in list(self.d1 & self.d2):
            if self.d1.getMd5ByFileItem(item) != self.d2.getMd5ByFileItem(item):
                _tmpLs.append(item)
        self.progress.update(self.pid, total=len(_tmpLs))
        self.progress.start()
        self.progress.start_task(self.pid)

        for item in _tmpLs:
            self.jobLs.append(self.pool.submit(self._run, item))

        DiffFilesToStructHtml.wait(self.jobLs)
        self.progress.stop()

        with open(os.path.join(self.rt, "README.md"), "w") as f:
            print("# Diff Results | 目录对比结果", file=f, end="\n\n")

            print(
                "## Several documents with differences as shown in the table below"
                if user_lang != "zh"
                else "## 存在若干有差异的文件如下表",
                file=f,
                end="\n\n",
            )

            print(
                f'|{"Path" if user_lang != "zh" else "路径"}|{"Results Link" if user_lang != "zh" else "结果链接"}|\n|---|:---:|',
                file=f,
            )
            for item in sorted(_tmpLs):
                print(
                    f'|{item}|[{"result" if user_lang != "zh" else "结果"}](file://{self.rt + item + ".html"})|',
                    file=f,
                )

            print(
                "## There are several non-shared documents as shown in the table below"
                if user_lang != "zh"
                else "## 存在若干非共有文件如下表",
                file=f,
                end="\n\n",
            )

            print(f"|{self.d1.name}|{self.d2.name}|\n|---|---|", file=f)
            for item in sorted(list(self.d1 ^ self.d2)):
                print(
                    f'|{item if item in self.d1 else " "}|{item if item in self.d2 else " "}|',
                    file=f,
                )
