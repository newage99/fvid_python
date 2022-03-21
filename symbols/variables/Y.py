from symbols.Variable import Variable


class Y(Variable):

    @staticmethod
    def symbol() -> str:
        return "y"

    @staticmethod
    def compute(x, y, n):
        return y
