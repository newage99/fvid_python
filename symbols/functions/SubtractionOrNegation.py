from symbols.Function import Function


class SubtractionOrNegation(Function):

    @staticmethod
    def symbol() -> str:
        return "-"

    @staticmethod
    def compute(variables: list):
        if len(variables) > 1:
            result = 0
            for var in variables:
                result -= var
            return result
        else:
            return -variables[0]
