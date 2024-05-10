from enum import Enum


class loan_status(Enum):
    """ Enum for loan Status."""
    pending = "PENDING"
    approved = "APPROVED"
    paid = "PAID"


class emi_status(Enum):
    """ Enum for EMI status."""
    pending = "PENDING"
    paid = "PAID"
