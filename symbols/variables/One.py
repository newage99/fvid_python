from symbols.Variable import Variable


class One(Variable):

    @staticmethod
    def symbol() -> str:
        return "1"

    @staticmethod
    def compute(x, y, n):
        return 1
