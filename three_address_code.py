from parser import code_generator


def write_code_to_file(address):
    with open(address, 'w') as f:
        for tac in code_generator.program_block:
            f.write(f'{tac.opno}\t({tac.operation}, {tac.lhs}, {tac.rhs}, {tac.target})')


class ThreeAddressCode:
    def __init__(self, opno, operation, lhs='', rhs='', target='') -> None:
        self.operation = operation
        self.lhs = lhs
        self.rhs = rhs
        self.target = target
        self.opno = opno

