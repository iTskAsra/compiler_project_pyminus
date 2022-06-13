
class ThreeAddressCode:
    def __init__(self, opno, operation, lhs='', rhs='', target='') -> None:
        self.operation = operation
        self.lhs = lhs
        self.rhs = rhs
        self.target = target
        self.opno = opno
