from sqlalchemy import Column, Integer, Enum, ForeignKey
from app import db
from common.common import loan_status


class Loan(db.Model):
    __tablename__ = 'loan'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    term = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    status = Column(Enum(loan_status), nullable=False)
