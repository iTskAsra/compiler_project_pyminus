class symbol:
    def __init__(self, symbol_name='UNKNOWN', symbol_type='UNDEFINED', data_block_address=0) -> None:
        self.data_block_address = data_block_address
        self.symbol_name = symbol_name
        self.symbol_type = symbol_type
        self.array_length = 0
        self.address_assigned = False

    def __repr__(self) -> str:
        return f'type: {self.symbol_type} --- name: {self.symbol_name} --- pointer: {self.data_block_address}'

    def has_valid_address(self):
        return self.address_assigned