from flask import jsonify
from app import db
from datetime import timedelta, date
from models.loan import Loan
from models.emi import EMI

from common.common import loan_status, emi_status


def view_loans(user_id, status=None):
    """ Get the customer's loans as per the status/all. """

    loan_query = Loan.query.filter_by(user_id=user_id)
    if status:
        loan_query = loan_query.filter_by(status=status)
    loans = loan_query.all()

    response = {"data": []}

    for loan in loans:
        loan_data = {"Amount": loan.amount,
                     "Status": loan.status.value}
        response["data"].append(loan_data)

    return jsonify(response)


def repay_emi(loan_id, amount, user_id):
    """ update the EMI/Loan status of the given loan. """
    loan = Loan.query.filter_by(id=loan_id, user_id=user_id).first()
    if not loan:
        return "invalid loan repayment", 400
    if loan.status == loan_status.paid:
        return "Loan is already Paid", 400

    emis = EMI.query.filter_by(loan_id=loan_id, status=emi_status.pending,).order_by(EMI.loan_date).all()

    if not emis:
        return "No EMI found.", 400

    if amount < emis[0].amount:
        return "Repay amount is less than the EMI amount", 400

    emis[0].status = emi_status.paid

    if len(emis) == 1:
        loan.status = loan_status.paid

    db.session.commit()

    response = "EMI repayment is successful."

    if loan.status == loan_status.paid:
        response += " Loan is paid successfully."

    return response


def create_new_loan(amount, term, user_id):
    """ Create new loan request for the customer. """
    loan = Loan(user_id=user_id, amount=amount, term=term, status=loan_status.pending)
    db.session.add(loan)
    db.session.commit()

    response = f"Loan of amount {amount} has been created successfully for {term} term"

    return response


def admin_approve_loan(loan_id):
    """ Admin changes the status of the given loan. """
    loan = Loan.query.filter_by(id=loan_id).first()
    if not loan or loan.status != loan_status.pending:
        return "Invalid loan approval"

    loan.status = loan_status.approved
    terms = loan.term
    loan_date = date.today()
    emi_amount = round(loan.amount / terms, 2)
    term = 1
    while term <= terms:
        emi = EMI(loan_id=loan.id, status=emi_status.pending,
                  loan_date=loan_date + timedelta(days=term * 7),
                  amount=emi_amount)
        db.session.add(emi)
        term += 1
    db.session.commit()

    response = f"Loan has been approved successfully"
    return response
