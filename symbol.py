class symbol:
    def __init__(self, symbol_name='UNKNOWN', symbol_type='UNDEFINED', data_block_offset=0) -> None:
        self.data_block_offset = data_block_offset
        self.symbol_name = symbol_name
        self.symbol_type = symbol_type

    def __repr__(self) -> str:
        return f'type: {self.symbol_type} --- name: {self.symbol_name} --- pointer: {self.stack_pointer}'
