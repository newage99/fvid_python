import math

from symbols.Function import Function


class DivisionOrSquareRoot(Function):

    @staticmethod
    def does_parameters_order_affects_result() -> bool:
        return True

    @staticmethod
    def symbol() -> str:
        return "/"

    @staticmethod
    def compute(variables: list):

        if len(variables) > 1:
            result = variables[0]
            for i in range(1, len(variables)):
                if variables[i] != 0:
                    result //= variables[i]
            return result
        elif variables[0] >= 0:
            return math.isqrt(variables[0])
        return variables[0]
