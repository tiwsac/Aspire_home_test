from flask_httpauth import HTTPBasicAuth
from flask import request, g
from app import app, db
from controllers.loan import *
from controllers.user import *

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/create/user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    is_admin = request.json.get('isAdmin') or False
    if username is None or password is None:
        return "Missing parameter", 400

    return create_new_user(username=username, password=password, is_admin=is_admin)


@app.route('/api/user/getLoan', methods=['POST'])
@auth.login_required
def get_loan():
    if g.user.is_admin:
        return "Invalid user", 400
    amount = request.json.get('amount')
    term = request.json.get('term')

    if amount is None or term is None:
        return "Missing parameter", 400

    if term is None or term == 0:
        return "Invalid Parameter", 400

    return create_new_loan(amount=amount, term=term, user_id=g.user.id)


@app.route('/api/user/viewLoan')
@auth.login_required
def view_loan():
    if g.user.is_admin:
        return "Invalid user", 400

    # Status is optional parameter
    status = request.json.get('status')
    return view_loans(status=status, user_id=g.user.id)


@app.route('/api/user/repayLoan', methods=['PUT'])
@auth.login_required
def repay_loan():
    if g.user.is_admin:
        return "Invalid user", 400

    loan_id = request.json.get('id')
    amount = request.json.get('amount')
    return repay_emi(loan_id=loan_id, amount=amount, user_id=g.user.id)


@app.route('/api/user/approveLoan', methods=['PUT'])
@auth.login_required
def approve_loan():
    if not g.user.is_admin:
        return "Invalid non-Admin user", 400
    loan_id = request.json.get('id')
    if loan_id is None:
        return "Missing parameter", 400
    return admin_approve_loan(loan_id=loan_id)
