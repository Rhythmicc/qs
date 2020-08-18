# coding=utf-8
from colorama import Back, Style
import math


class RollBar:
    def __init__(self, values: list, max_: int = 100, height: int = 10):
        """
        滚动柱状图初始化

        Rolling histogram initialization

        :param values: 值列表
        :param max_: 最大值
        :param height: 高度
        """
        self._title = ''
        self.max_ = max_
        self.width = len(values)
        self.height = height
        self.canvas = [[] for ignore in range(height)]
        for val in values:
            cur = math.ceil(val / max_ * height)
            for _i in range(cur):
                self.canvas[_i].append(Back.GREEN + ' ' + Style.RESET_ALL)
            for _i in range(cur, height):
                self.canvas[_i].append(Style.RESET_ALL + ' ')

    def __str__(self):
        """
        返回字符串形式的图

        Returns a graph as a string

        :return: 字符串形式的图
        """
        if self.title:
            title_idx = (self.width - len(self._title)) // 2 + 1
            title_idx = max(title_idx, 0)
            res = ' ' * title_idx + self._title + '\n'
        else:
            res = ''
        return res+'100%%%s' % ('_' * (self.width+1)) + '\n    │' + '\n    │'.join(
            [''.join(i) for i in self.canvas[::-1]]) + '\n  0%╂' + '────┴' * math.ceil(self.width // 5)

    def show(self):
        """
        打印柱状图

        Print the bar chart

        :return: None
        """
        print(self)

    def add(self, val: float):
        """
        扔掉第一个值，并在尾部添加val

        Drop the first value and add Val at the end

        :param val: 值
        :return: None
        """
        for _i in self.canvas:
            _i.pop(0)
        cur = math.ceil(val / self.max_ * self.height)
        for _i in range(cur):
            self.canvas[_i].append(Back.GREEN + ' ' + Style.RESET_ALL)
        for _i in range(cur, self.height):
            self.canvas[_i].append(Style.RESET_ALL + ' ')

    def title(self, _title: str):
        """
        设置柱状图的标题

        Sets the title of the bar chart

        :param _title: 标题
        :return: None
        """
        self._title = _title

    def set(self, vals: list):
        """
        设置柱状图的全部值

        Sets all values of the histogram

        :param vals: 值列表
        :return: None
        """
        for i in self.canvas:
            i.clear()
        for val in vals:
            cur = math.ceil(val / self.max_ * self.height)
            for _i in range(cur):
                self.canvas[_i].append(Back.GREEN + ' ' + Style.RESET_ALL)
            for _i in range(cur, self.height):
                self.canvas[_i].append(Style.RESET_ALL + ' ')
