import pytest

from main import db, app
from controllers.loan import *
from models.loan import Loan
from models.emi import EMI
from flask import jsonify
from datetime import timedelta, date


@pytest.fixture
def app_context():
    with app.app_context():
        yield


@pytest.mark.parametrize(
    ("amount", "term", "user_id", "message"),
    (
        (3000, 3, 0, "Loan of amount 3000 has been created successfully for 3 term"),
    ),
)
def test_create_loan(app_context, amount, term, user_id, message):
    """ Unit test for create loan. """
    response = create_new_loan(amount=amount, term=term, user_id=user_id)
    loan_query = Loan.query.filter(Loan.user_id == user_id)
    loan = loan_query.first()
    loan_query.delete()
    db.session.commit()
    assert response == message
    assert loan.status == loan_status.pending


@pytest.mark.parametrize(
    ("amount", "term", "user_id", "message"),
    (
        (3000, 3, 0, "Loan of amount 3000 has been created successfully for 3 term"),
    ),
)
def test_view_loan(app_context, amount, term, user_id, message):
    """ Unit test for view loans. """
    user_id = 0
    create_new_loan(amount=amount, term=term, user_id=user_id)
    response = view_loans(user_id=user_id).get_json()['data']
    Loan.query.filter(Loan.user_id == user_id).delete()
    db.session.commit()
    assert response[0]["Amount"] == amount
    assert response[0]["Status"] == loan_status.pending.value


@pytest.mark.parametrize(
    ("amount", "term", "user_id", "message"),
    (
        (3000, 1, 0, "Loan has been approved successfully"),
    ),
)
def test_approve_loan_success(app_context, amount, term, user_id, message):
    """ Unit test for approve loans. """
    response = create_new_loan(amount=amount, term=term, user_id=user_id)
    loan_query = Loan.query.filter(Loan.user_id == user_id)
    loan = loan_query.first()
    response = admin_approve_loan(loan_id=loan.id)
    emi_query = EMI.query.filter(EMI.loan_id == loan.id)
    emi = emi_query.first()
    loan_query.delete()
    emi_query.delete()
    db.session.commit()
    emi_date = date.today() + timedelta(days=7)
    assert response == message
    assert loan.status == loan_status.approved
    assert emi.status == emi_status.pending
    assert emi.loan_date == emi_date


@pytest.mark.parametrize(
    ("loan_id", "message"),
    (
        (None, "Invalid loan approval"),
        (0, "Invalid loan approval"),
    ),
)
def test_approve_loan_failure(app_context, loan_id, message):
    """ Unit test for approve loans when invalid loan-id is provided """
    response = admin_approve_loan(loan_id=loan_id)
    assert response == message


@pytest.mark.parametrize(
    ("amount", "term", "user_id", "message1", "message2", "message3"),
    (
        (3000, 1, 0,
         "Repay amount is less than the EMI amount",
         "EMI repayment is successful. Loan is paid successfully.",
         "Loan is already Paid"),
    ),
)
def test_repay_loan_success(app_context, amount, term, user_id, message1, message2, message3):
    """ Unit test for repay loans. """
    response = create_new_loan(amount=amount, term=term, user_id=user_id)
    loan_query = Loan.query.filter(Loan.user_id == user_id)
    loan = loan_query.first()
    admin_approve_loan(loan_id=loan.id)
    response1 = repay_emi(loan_id=loan.id, amount=amount - 10, user_id=user_id)
    response2 = repay_emi(loan_id=loan.id, amount=amount, user_id=user_id)
    response3 = repay_emi(loan_id=loan.id, amount=amount, user_id=user_id)
    emi_query = EMI.query.filter(EMI.loan_id == loan.id)
    emi = emi_query.first()
    loan_query.delete()
    emi_query.delete()
    db.session.commit()
    emi_date = date.today() + timedelta(days=7)
    assert response1[0] == message1
    assert response2 == message2
    assert response3[0] == message3
    assert loan.status == loan_status.paid
    assert emi.status == emi_status.paid


@pytest.mark.parametrize(
    ("loan_id", "amount", "term", "user_id", "message"),
    (
        (None, 3000, 1, 0, "invalid loan repayment"),
        (0, 3000, 1, 0, "invalid loan repayment"),
        (2, 3000, 1, 0, "invalid loan repayment"),
    ),
)
def test_repay_loan_failure(app_context, loan_id, amount, term, user_id, message):
    """ Unit test for repay loans. """
    response = repay_emi(loan_id=loan_id, amount=amount, user_id=user_id)
    assert response[0] == message