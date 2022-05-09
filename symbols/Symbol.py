from misc.globals import get_symbol_classes_that_inherit_from
import abc


class Symbol:

    __symbols_dict = None
    __symbols_list = None
    __symbols_strs = None

    @staticmethod
    @abc.abstractmethod
    def symbol() -> str:
        pass

    @staticmethod
    def symbols_dict():
        if not Symbol.__symbols_dict:
            Symbol.__symbols_dict = get_symbol_classes_that_inherit_from("Symbol", "symbol")
        return Symbol.__symbols_dict

    @staticmethod
    def symbols():
        if not Symbol.__symbols_list:
            Symbol.__symbols_list = []
            symbols_dict = Symbol.symbols_dict()
            for value in symbols_dict.values():
                Symbol.__symbols_list.append(value)
        return Symbol.__symbols_list

    @staticmethod
    def symbols_strs() -> list:
        if not Symbol.__symbols_strs:
            return list(Symbol.symbols_dict().keys())
        return Symbol.__symbols_strs

    @staticmethod
    def get_symbol_by_str(value: str):
        symbols = Symbol.symbols()
        for symbol in symbols:
            if symbol.symbol() == value:
                return symbol
        return None

    def __str__(self):
        return self.symbol()
