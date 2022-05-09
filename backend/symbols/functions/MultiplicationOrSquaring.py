from symbols.Function import Function


class MultiplicationOrSquaring(Function):

    @staticmethod
    def does_parameters_order_affects_result() -> bool:
        return False

    @staticmethod
    def symbol() -> str:
        return "*"

    @staticmethod
    def compute(variables: list):
        if len(variables) > 1:
            result = variables[0]
            for i in range(1, len(variables)):
                result *= variables[i]
            return result
        return variables[0] * variables[0]
