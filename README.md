# Aspire_home_test

## Setup

After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt

## Running

To run the server use the following command:

    (venv) $ python main.py

     * Running on http://127.0.0.1:5008/
     * Restarting with reloader

Then from a different terminal window you can send requests.

## Running Tests

To run the all tests use the following command:

    (venv) $ pytest tests/
    
To run the one test-file use the following command:

    (venv) $ pytest tests/unit/test_loan_controller.py

To run the one test from a file use the following command:

    (venv) $ pytest tests/unit/test_loan_controller.py::test_approve_loan_failure

## API Documentation

POST */api/create/users*

	curl --location 'http://127.0.0.1:5008/api/create/user' \
	--header 'Content-Type: application/json' \
	--data '{"username":"test_admin","password":"python", "isAdmin": true   }'

Register a new user. For admin users we have to provide isAdmin flag 'True'. isAdmin flag is optional and default value is False. It means non-admin user. Only admin user can approve the loan and non admin user can apply for loan and repay the EMIs.
    
    
POST */api/user/getLoan*

	curl --location 'http://127.0.0.1:5008/api/user/getLoan' \
	--header 'Content-Type: application/json' \
	--header 'Authorization: Basic dGVzdF91c2VyOnB5dGhvbg==' \
	--data '{"amount": 6000,"term": 3}'

Only Non-admin users can create loan. It will create a loan entry in our Database with pending state. Only Admin user can approve it. After approval user can repay the EMIs
    
GET */api/user/viewLoan*

	curl --location --request GET 'http://127.0.0.1:5008/api/user/viewLoan' \
	--header 'Content-Type: application/json' \
	--header 'Authorization: Basic dGVzdF91c2VyOnB5dGhvbg==' \
	--data '{"status": "pending"}'

Only Non-admin users can view their loans. It will show the loans as per the status provided. If status not provided it will show all the loans belong to the user.
    
POST */api/user/approveLoan*

	curl --location --request PUT 'http://127.0.0.1:5008/api/user/approveLoan' \
	--header 'Content-Type: application/json' \
	--header 'Authorization: Basic dGVzdF9hZG1pbjpweXRob24=' \
	--data '{"id": 1}'

Only admin users can any loan as per the ID provided. It will change the status of given loan from pending to approved. It will create weekly EMIs as for the given term. For above curl it will create 3 EMIs for 2000, first EMI starts from next week. We will create EMIs entry in the EMI table as pending-status.
    
POST /api/user/repayLoan**

	curl --location --request PUT 'http://127.0.0.1:5008/api/user/repayLoan' \
	--header 'Content-Type: application/json' \
	--header 'Authorization: Basic dGVzdF91c2VyOnB5dGhvbg==' \
	--data '{"id": "1", "amount": 4000}'

Only Non-admin users can repay the loan's EMI. It will change the status of given loan's upcoming EMI status from pending to paid. Once last EMI is paid we update the loan status from approved to paid in loan table.



