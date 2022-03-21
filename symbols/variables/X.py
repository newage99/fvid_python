from symbols.Variable import Variable


class X(Variable):

    @staticmethod
    def symbol() -> str:
        return "x"

    @staticmethod
    def compute(x, y, n):
        return x
