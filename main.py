import os
from app import app, db
from routes.user import *

# extensions

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5008, use_reloader=True)