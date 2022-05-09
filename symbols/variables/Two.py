from symbols.Variable import Variable


class Two(Variable):

    @staticmethod
    def symbol() -> str:
        return "2"

    @staticmethod
    def compute(x, y, n):
        return 2
