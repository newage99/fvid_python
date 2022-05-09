from symbols.Variable import Variable


class NumberOfNodes(Variable):

    @staticmethod
    def symbol() -> str:
        return "n"

    @staticmethod
    def compute(x, y, n):
        return n
