class symbol:
    def __init__(self, symbol_name = 'UNKNOWN', symbol_type = 'UNDEFINED', stack_pointer = None) -> None:
        self.stack_pointer = stack_pointer
        self.symbol_name = symbol_name
        self.symbol_type = symbol_type

    def __repr__(self) -> str:
        return f'type: {self.symbol_type} --- name: {self.symbol_name} --- pointer: {self.stack_pointer}'