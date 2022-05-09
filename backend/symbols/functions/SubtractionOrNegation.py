from symbols.Function import Function


class SubtractionOrNegation(Function):

    @staticmethod
    def does_parameters_order_affects_result() -> bool:
        return True

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
