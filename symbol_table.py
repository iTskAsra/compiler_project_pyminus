from symbol import symbol

class symbol_table:
    def __init__(self) -> None:
        self.symbols = []

    def add_symbol(self, symbol_name, symbol_type):
        if not self.is_symbol_new(symbol_name):
            return
        
        symbol_to_be_added = symbol(symbol_name, symbol_type)
        self.symbols.append(symbol_to_be_added)

    def is_symbol_new(self, symbol_name):
        for symbol in self.symbols:
            if symbol.symbol_name == symbol_name:
                return False
        
        return True