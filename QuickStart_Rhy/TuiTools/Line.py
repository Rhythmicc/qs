import diagram
import io


class Line:
    def __init__(self, values, height, width):
        self.values = values
        self.width = height
        self.height = width

    def __str__(self):
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

    def push(self, x):
        self.values.append(x)

    def pop(self):
        self.values.pop(0)
