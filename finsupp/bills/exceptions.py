class BillError(Exception):
    pass


class BillNotFound(BillError):
    pass


class BillAlreadyPaid(BillError):
    pass


class BillPaymentError(BillError):
    pass
