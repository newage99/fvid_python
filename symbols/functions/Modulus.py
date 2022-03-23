from symbols.Function import Function


class Modulus(Function):

    @staticmethod
    def symbol() -> str:
        return "%"

    @staticmethod
    def compute(variables: list):
        result = variables[0]
        for i in range(1, len(variables)):
            if variables[i] != 0:
                result %= variables[i]
        return result
