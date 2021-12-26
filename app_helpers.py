import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

# Direct the user to an HTML page that ouputs an error message along with the code 400
def error_message(message, code=400):
    return render_template("error.html", number=code, message=message)

# This function decorates routes to require login. Taken from this link: https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function