import abc

from misc.globals import get_symbol_classes_that_inherit_from

from symbols.Symbol import Symbol


class Variable(Symbol, abc.ABC):

    __symbols_dict = None
    __symbols_list = None
    __symbols_strs = None

    @staticmethod
    @abc.abstractmethod
    def compute(x, y, n):
        pass

    @staticmethod
    def symbols_dict() -> dict:
        if not Variable.__symbols_dict:
            Variable.__symbols_dict = get_symbol_classes_that_inherit_from("Variable", "symbol")
        return Variable.__symbols_dict

    @staticmethod
    def symbols() -> list:
        if not Variable.__symbols_list:
            Variable.__symbols_list = []
            symbols_dict = Variable.symbols_dict()
            for value in symbols_dict.values():
                Variable.__symbols_list.append(value)
        return Variable.__symbols_list

    @staticmethod
    def symbols_strs() -> list:
        if not Variable.__symbols_strs:
            return list(Variable.symbols_dict().keys())
        return Variable.__symbols_strs
