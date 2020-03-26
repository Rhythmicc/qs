from colorama import Back, Style
import math


class RollBar:
    def __init__(self, values, max_=100, height=10):
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
        if self.title:
            title_idx = (self.width - len(self._title)) // 2 + 1
            title_idx = max(title_idx, 0)
            res = ' ' * title_idx + self._title + '\n'
        else:
            res = ''
        return res+'100%%%s' % ('_' * (self.width+1)) + '\n    │' + '\n    │'.join(
            [''.join(i) for i in self.canvas[::-1]]) + '\n  0%╂' + '────┴' * math.ceil(self.width // 5)

    def show(self):
        print(self)

    def add(self, val):
        for _i in self.canvas:
            _i.pop(0)
        cur = math.ceil(val / self.max_ * self.height)
        for _i in range(cur):
            self.canvas[_i].append(Back.GREEN + ' ' + Style.RESET_ALL)
        for _i in range(cur, self.height):
            self.canvas[_i].append(Style.RESET_ALL + ' ')

    def title(self, _title: str):
        self._title = _title

    def set(self, vals):
        for i in self.canvas:
            i.clear()
        for val in vals:
            cur = math.ceil(val / self.max_ * self.height)
            for _i in range(cur):
                self.canvas[_i].append(Back.GREEN + ' ' + Style.RESET_ALL)
            for _i in range(cur, self.height):
                self.canvas[_i].append(Style.RESET_ALL + ' ')
