# coding=utf-8
import diagram
import io


class Line:
    def __init__(self, values: list, height: int, width: int):
        """
        折线图

        line chart

        :param values: 值列表
        :param height: 高度
        :param width: 宽度
        """
        self.values = values
        self.width = height
        self.height = width

    def __str__(self):
        """
        绘图并返回字符串

        Draw and return a string

        :return: 折线图的字符串
        """
        opt = diagram.DOption()
        opt.size = diagram.Point([self.height, self.width])
        opt.mode = 'g'
        stream = io.BytesIO()
        gram = diagram.DGWrapper(
            data=[self.values, range(len(self.values))],
            dg_option=opt,
            ostream=stream
        )
        gram.show()
        return str(stream.getvalue(), encoding="utf-8")

    def push(self, x: float):
        """
        尾部添加值

        Tail add value

        :param x: 值
        :return: None
        """
        self.values.append(x)

    def pop(self):
        """
        删除首部值

        Delete bow value

        :return: None
        """
        self.values.pop(0)
