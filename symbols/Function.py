import abc

from misc.globals import get_symbol_classes_that_inherit_from

from symbols.Symbol import Symbol


class Function(Symbol, abc.ABC):

    __symbols_dict = None
    __symbols_list = None
    __symbols_strs = None

    @staticmethod
    @abc.abstractmethod
    def compute(variables: list):
        pass

    @staticmethod
    def symbols_dict():
        if not Function.__symbols_dict:
            Function.__symbols_dict = get_symbol_classes_that_inherit_from("Function", "symbol")
        return Function.__symbols_dict

    @staticmethod
    def symbols():
        if not Function.__symbols_list:
            Function.__symbols_list = []
            symbols_dict = Function.symbols_dict()
            for value in symbols_dict.values():
                Function.__symbols_list.append(value)
        return Function.__symbols_list

    @staticmethod
    def symbols_strs() -> list:
        if not Function.__symbols_strs:
            return list(Function.symbols_dict().keys())
        return Function.__symbols_strs
