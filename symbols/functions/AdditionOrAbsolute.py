from symbols.Function import Function


class AdditionOrAbsolute(Function):

    @staticmethod
    def symbol() -> str:
        return "+"

    @staticmethod
    def compute(variables: list):
        if len(variables) > 1:
            result = 0
            for var in variables:
                result += var
            return result
        else:
            if variables[0] < 0:
                return -variables[0]
            return variables[0]
