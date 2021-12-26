# Execute the following command in your codespace terminal: "pip install yfinance"
# Execute the following command in your codespace terminal: "pip install numpy"
# Execute the following command in your codespace terminal: "pip install pip install matplotlib"

# Execute the following command in your codespace terminal: "export FLASK_APP=my_app.py"
# Then execute "flask run"

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

import yfinance as yf

from datetime import datetime

from app_helpers import error_message, login_required

# Configure application
my_app = Flask(__name__)


# Ensure templates are auto-reloaded
my_app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
my_app.config["SESSION_PERMANENT"] = False
my_app.config["SESSION_TYPE"] = "filesystem"
Session(my_app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@my_app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# This function directs user to the homepage
@my_app.route("/")
@login_required
def homepage():
    return render_template("homepage.html")



@my_app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":

        # Ensure every field is not blank
        if not request.form.get("username"):
            return error_message("must create a username", 400)
        elif not request.form.get("password"):
            return error_message("must create a password", 400)
        elif not request.form.get("confirmation"):
            return error_message("must confirm password", 400)
        
        # If password and confirmation don't match return an error
        if request.form.get("password") != request.form.get("confirmation"):
            return error_message("passwords do not match", 400)
        
        # If username is already taken, return an error
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 1:
            return error_message("username already exists", 400)
        
        # Generate a hash of the user's password
        hashed_password = generate_password_hash(request.form.get("password"))

        # Add user to database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashed_password)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Log User in
        session["user_id"] = rows[0]["id"]

        return redirect("/")


@my_app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error_message("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error_message("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error_message("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@my_app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@my_app.route("/stock", methods=["GET", "POST"])
def stock():

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("stock.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":

        # Get user input for a specific stock
        ticker = str(request.form.get("symbol"))
        ticker = ticker.upper()

        # Get stock data from Yahoo Finance
        stock_data_yfinance = yf.Ticker(ticker)
        stock_info = stock_data_yfinance.info

        # Check if the user inputted a valid ticker. If not, return an error message
        try:
            price = stock_info["currentPrice"]
        except KeyError:
            return error_message("Enter a valid ticker", 400)

        # Extract all the necessary numbers from yfinance
        stock_data = {
            "Name": stock_info["longName"],

            "Price": stock_info["currentPrice"],
            "EPS": stock_info["trailingEps"],
            "PE": None,

            "PB": stock_info["priceToBook"],

            "EVEBITDA": stock_info["enterpriseToEbitda"],

            "PS": stock_info["priceToSalesTrailing12Months"],

            "E-Growth": stock_info["earningsGrowth"],
            "PEG": None,

            "DY": stock_info["dividendYield"]
        }

        # Calculate the remaining financial metrics if possible.
        # If not possible, then just continue with the evaluation 
        try:
            stock_data["PE"] = stock_data["Price"] / stock_data["EPS"]
        except TypeError:
            pass

        try:
            stock_data["PEG"] = stock_data["PE"] / (stock_data["E-Growth"] * 100)
        except TypeError:
            pass

        # Create an empty dictionary that will soon hold only the financial ratios for the given stock 
        stock_metrics = {}

        # Copy over all the existing metrics from the original dictionary into a new dictionary.
        # If a metric was not able to be extracted, then just set the value of that metric in the new dictionary to N/A when copying it over 
        if stock_data["PE"] is None:
            stock_metrics["PE"] = "N/A"
            pass
        else:
            stock_metrics["PE"] = stock_data["PE"]

        if stock_data["PB"] is None:
            stock_metrics["PB"] = "N/A"
            pass
        else:
            stock_metrics["PB"] = stock_data["PB"]

        if stock_data["EVEBITDA"] is None:
            stock_metrics["EVEBITDA"] = "N/A"
            pass
        else:
            stock_metrics["EVEBITDA"] = stock_data["EVEBITDA"]

        if stock_data["PS"] is None:
            stock_metrics["PS"] = "N/A"
            pass
        else:
            stock_metrics["PS"] = stock_data["PS"]

        if stock_data["PEG"] is None:
            stock_metrics["PEG"] = "N/A"
            pass
        else:
            stock_metrics["PEG"] = stock_data["PEG"]

        if stock_data["DY"] is None:
            stock_metrics["DY"] = "N/A"
            pass
        else:
            stock_metrics["DY"] = stock_data["DY"]

        # Store the number of financial valuation metrics that will be used in a variable
        num_metrics = len(stock_metrics)

        # If there isn't enough financial data for the stock, don't evaluate it and return an error message
        if num_metrics < 4:
            return error_message("The stock could not be valued since the necessary financial information could not be found", 400)

        # Create a variable that represents the valuation score of a stock and initialize it to 0
        score = 0

        # At minimum, half of the metrics need to be deemed as good in order to value the stock as a buy
        minimum_score = num_metrics / 2

        # Look at each financial metric and increase the valuation score of the stock depending on each metric
        # Every metric will have an excellent, fair, and terrible scenario
        # For excellent scenarios, increase the score by 1. For fair scenarios, increase the score by 0.5. Don't increase the score for terrible scenarios

        # If the metric in question is not present in the dictionary, then skip over it and don't increase the score

        try:
            # The Price to Earnings ratio is excellent if it is less than 15, fair if between 15 and 18, and terrible if over 18
            if stock_metrics["PE"] < 15:
                score = score + 1
            elif stock_metrics["PE"] >= 15 and stock_metrics["PE"] <= 18:
                score = score + 0.5
        except (TypeError, KeyError):
            pass

        try:
            # The Price to Book ratio is excellent if it is under 1, fair if in between 1 and 3, and terrible if over 3
            if stock_metrics["PB"] < 1:
                score = score + 1
            elif stock_metrics["PB"] >= 1 and stock_metrics["PB"] <= 3:
                score = score + 0.5
        except (TypeError, KeyError):
            pass

        try:
            # The EV/EBITDA ratio is excellent if it is under 10, fair if in between 10 and 18.40, and terrible if over 18.40
            if stock_metrics["EVEBITDA"] < 10:
                score = score + 1
            elif stock_metrics["EVEBITDA"] >= 10 and stock_metrics["EVEBITDA"] <= 18.40:
                score = score + 0.5
        except (TypeError, KeyError):
            pass

        try:
            # The Price to Sales ratio is excellent if it is under 1, fair if in between 1 and 2, and terrible if over 2
            if stock_metrics["PS"] < 1:
                score = score + 1
            elif stock_metrics["PS"] >= 1 and stock_metrics["PS"] <= 2:
                score = score + 0.5
        except (TypeError, KeyError):
            pass

        try:
            # The Price to Earnings Growth ratio is excellent if it is under 1, fair if it is equal to 1, and terrible if over 1
            if stock_metrics["PEG"] < 1:
                score = score + 1
            elif stock_metrics["PEG"] == 1:
                score = score + 0.5
        except (TypeError, KeyError):
            pass

        try:
            # The Dividend Yield is excellent if it is higher than 6%, fair if it is between 2% and 6%, and terrible if under 2%
            if stock_metrics["DY"] > 0.06:
                score = score + 1
            elif stock_metrics["DY"] >= 0.02 and stock_metrics["DY"] <= 0.06:
                score = score + 0.5
        except (TypeError, KeyError):
            pass

        # If the calculated score is greater or equal to the minimum score needed to evaluate the stock as a buy, then direct the user to an HTML page that says the stock is a good buy.
        if score >= minimum_score:
            return render_template("yesbuy.html", name=stock_data["Name"], price=stock_data["Price"], pe=stock_metrics["PE"], pb=stock_metrics["PB"], evebitda=stock_metrics["EVEBITDA"], ps=stock_metrics["PS"], peg=stock_metrics["PEG"], dy=stock_metrics["DY"], score=score)
            # Render a template to buy the stock
        # Otherwise, direct the user to an HTML page that says the stock is not a good buy
        else:
            return render_template("nobuy.html", name=stock_data["Name"], price=stock_data["Price"], pe=stock_metrics["PE"], pb=stock_metrics["PB"], evebitda=stock_metrics["EVEBITDA"], ps=stock_metrics["PS"], peg=stock_metrics["PEG"], dy=stock_metrics["DY"], score=score)
            # Render a template to not buy the stock

@my_app.route("/investment", methods=["GET", "POST"])
def investment():

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("investment.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":

        # Get user input for a specific stock
        ticker = str(request.form.get("symbol"))
        ticker = ticker.upper()

        # Get stock data from Yahoo Finance
        stock_data_yfinance = yf.Ticker(ticker)
        stock_info = stock_data_yfinance.info

        # Check if the user inputted a valid ticker. If not, output an error message
        try:
            price = stock_info["currentPrice"]
        except KeyError:
            return error_message("Enter a valid ticker", 400)

        # Store the name of the company in a variable
        name = stock_info["longName"]

        # Get user inputs from the form and store it in variables
        # Make sure inputs are numeric. If not, display an error
        try:
            shares = float(request.form.get("num_shares"))
            if shares < 0:
                return error_message("Shares must be positive", 400)
        except ValueError:
            return error_message("You can't input characters in any field except the name field (besides 1 decimal point)", 400)

        try:
            buying = float(request.form.get("buy_price"))
            if buying < 0:
                return error_message("Buy Price must be positive", 400)
        except ValueError:
            return error_message("You can't input characters in any field except the name field (besides 1 decimal point)", 400)

        try:
            selling = float(request.form.get("sell_price"))
            if selling < 0:
                return error_message("Sell Price must be positive", 400)
        except ValueError:
            return error_message("You can't input characters in any field except the name field (besides 1 decimal point)", 400)
        
        try:
            dividends = float(request.form.get("dividends"))
            if dividends < 0:
                return error_message("Dividends must be positive", 400)
        except ValueError:
            return error_message("You can't input characters in any field except the name field (besides 1 decimal point)", 400)

        try:
            commissions = float(request.form.get("commissions"))
            if commissions < 0:
                return error_message("Commissions must be positive", 400)
        except ValueError:
            return error_message("You can't input characters in any field except the name field (besides 1 decimal point)", 400)

        # Calculate the change in share value
        change_in_share_value = (float(selling - buying)) * shares

        # Add dividends to the previous value and subtract comission costs
        numerator = float(change_in_share_value) + dividends - commissions

        # Initial investment value
        initial = float(shares) * buying

        # Calculate the return on investment
        roi = numerator / initial
        

        # The following three numbers were found on the internet. 
        # Average return rate for the S&P 500 Index
        sp500_return = 0.08
        # Current 10-year US Treasury Yield 
        treasury_yield = 0.0135
        # National average interest earned on a savings account
        savings_account_interest = 0.06

        # Convert the ROIs to percentages so they can be passed into the HTML file later on
        roi = roi * 100
        roi = round(roi, 2)
        sp500_return = sp500_return * 100
        treasury_yield = treasury_yield * 100
        savings_account_interest = savings_account_interest * 100

        # Code to create a bar chart was inspired by this website: https://pythonspot.com/matplotlib-bar-chart/
        # Create a bar graph with the four different ROIs
        objects = ('Your Investment', 'S&P 500', 'Treasury Yield', 'Savings Account')
        y_pos = np.arange(len(objects))
        performance = [roi, sp500_return, treasury_yield, savings_account_interest]

        # Change the apperance of the graph and label it to make it more viewable and easier to comprehend
        plt.clf()
        plt.bar(y_pos, performance, align='center', alpha=0.5, color=['green', 'red', 'blue', 'yellow'])
        plt.xticks(y_pos, objects)
        plt.ylabel('Return on Investment (%)')
        plt.xlabel('Type of Investment')
        plt.title('FinAn\'s Investment Analysis - Visualization')

        # Save the graph as a local file in the current directory
        plt.savefig("analysis.png", bbox_inches="tight", pad_inches=1)

        # If the calculated ROI is greater than or equal to every other form of ROI, then direct the user to an HTML page that says their investment was a good one
        if roi >= sp500_return and roi >= treasury_yield and roi >= savings_account_interest:
            return render_template("goodroi.html", name=name, roi=roi)
        # Otherwise, direct the user to an HTML page that says their investment was not a good one since their money could have been invested elsewhere to make higher returns
        else:
            return render_template("badroi.html", name=name, roi=roi)


# Allows the user to create a post.
@my_app.route("/createpost", methods=["GET", "POST"])
def createpost():
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("createpost.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        post_text = request.form.get("message")

        # Ouput an error if the user is trying to post without typing anything
        if not post_text:
            return error_message("You must type at least 1 character in the text field", 400)
        else:
            # Get the user's username
            row = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
            user_name = row[0]["username"]
            user_name = str(user_name)

            # Insert a new row into the forum table that has the user's post
            db.execute("INSERT INTO forum (username, post, timestamp) VALUES (?, ?, ?)", user_name, post_text, str(datetime.now()))

            # Get all the posts from the forum table, pass it into an HTML page to display all of the posts to the user, and direct the user to that HTML page
            forum = db.execute("SELECT * FROM forum")
            return render_template("discussion.html", forum=forum)


# This function displays the discussion board in case the user clicks the Discussion Forum link on the top of the page
@my_app.route("/forum")
def forum():
    # Get all the posts from the forum table, pass it into an HTML page to display all of the posts to the user, and direct the user to that HTML page
    forum = db.execute("SELECT * FROM forum")
    return render_template("discussion.html", forum=forum)

# This function directs the user to an HTML page that educates them about finance, namely stock evaluation and investment analysis
@my_app.route("/education")
def education():
    return render_template("education.html")

# In case of an error that was not counted for, display a generic error to the user
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error_message("Something went wrong", 400)



# Listen for errors
for code in default_exceptions:
    my_app.errorhandler(code)(errorhandler)