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
        for s in self.symbols:
            if s.symbol_name == symbol_name:
                return False

        return True

    def find_address(self, symbol_name):
        for s in self.symbols:
            if s.symbol_name == symbol_name:
                return s.data_block_offset


    def symbol_has_address(self, symbol_name):
        for s in self.symbols:
            if s.symbol_name == symbol_name:
                return s.has_valid_address()


    def set_symbol_address(self, symbol_name, address):
        for s in self.symbols:
            if s.symbol_name == symbol_name:
                s.data_block_address = address
