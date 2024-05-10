from sqlalchemy import Column, Integer, Enum, ForeignKey, Date, Float
from app import db
from common.common import emi_status


class EMI(db.Model):
    __tablename__ = 'emi'

    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey("loan.id"), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(emi_status), index=True, nullable=False)
    loan_date = Column(Date, nullable=False)
