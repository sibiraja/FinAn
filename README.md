Project: FinAn

Video link: https://youtu.be/3BiwdxRVAxM

This is FinAn! To get started, you will need to manually execute the following commands in the /final folder:
- pip install yfinance
- pip install numpy
- pip install pip install matplotlib

These commands will install the python packages that are needed to allow FinAn to work properly. Once done with that, manually execute the following commands in the /final folder to start using FinAn:
- export FLASK_APP=my_app.py
- flask run

Click on the link that pops up to get directed to the login page of FinAn. Because you do not have an existing account, click the Register link located on the top right of the page to get directed to the register page. On the Register page, there is a form that accepts three fields: username, password, and password confirmation. Enter in a username and password (and re-enter the password in the password confirmation field) to create an account. An error message will be outputted if any of the fields are left blank, if the passwords do not match, or if there is an already existing account with that username. After passing these checks, you will be taken to the home page of the application.

On this page, there are five links at the top of the page (Stock Evaluation, Investment Analysis, Create a Post, Discussion Forum, Learn about Finance), along with FinAn's logo and the logout link. At any time while logged in, clicking on the logo will take you back to the home page, while clicking the login link will log you out of your account. You will have to log back in or create another account using the register link to continue using FinAn. 

Clicking the Stock Evaluation link at the top of the page will take you to the stock evaluation component of the application. On this page, there is a form that asks for a stock symbol of a company. Here, you can input the ticker symbol of any American stock to evaluate the company. If the ticker symbol is invalid, then an error is displayed. If the ticker symbol is valid, then FinAn will evaluate the stock for you by analyzing various financial multiples/ratios of the company. After the evaluation is complete, you are then directed to a page that displays the company name, current share price, its financial ratios, FinAn's calculated score for the company's stock, and whether or not the company's stock is currently a good buy.

Clicking on the Investment Analysis link at the top of the page will take you to the investment analysis component of the application. On this page, there is a form that asks for various pieces of information that pertain to a stock investment that you made: the company's ticker symbol, number of shares that you bought, the price that you bought the shares at, the price that you sold the shares at, any dividends that you earned, and any commission costs that were associated with the entire investment process. An error message will be outputted if any of the following conditions occur:
-  one or more fields is left blank
- the ticker symbol is invalid
- characters besides numbers and one decimal point is inputted in the Number of Shares, Buy Price, Sell Price, Earned Dividends, and/or Commission Costs fields
- if negative numbers are entered in the Number of Shares, Buy Price, Sell Price, Earned Dividends, and/or Commission Costs fields

If the form is submitted without any errors, then you are taken to a page that displays the analysis conducted on your investment by FinAn. On this page, the company name, as well as the return that you made on the investment, is displayed. Underneath that, the returns that could have been made on other forms of investments are displayed. Following that, FinAn's analysis is displayed, which describes whether or not your investment was good based on the returns that could have been made through other forms of investments. Beneath that is a message that tells you to open a visualization of FinAn's analysis of your investment. Located in the /final folder is a file called analysis.png. Opening the file should show you a graphical representation of your return on investment (ROI) compared to the ROI of other forms of investments.

Clicking on the Create a Post link at the top of the page will take you to a page that is part of the Discussion Forum component of FinAn. Here, there is a form that asks for you to type a message. Trying to submit the form without typing in a message will output an error message. After typing a message, you can click the Submit Post button to post your message to the Discussion Forum. You are then taken to the Discussion Forum page, which displays a table that contains every post that has been submitted to the Discussion Forum, along with the post that you just created. For every post that has been submitted the following information is displayed in a table format:
- the username of the user that created the post
- the post itself
- the date and time at which the post was created

You can click on the Discussion Forum link at any time while using FinAn to arrive at the same page just described. 

Finally, clicking on the Learn about Finance link will take you to a page that educates you about stock evaluation and investment analysis. In the middle of the page are rows that pertain to a specific financial multiple. Clicking on a row will expand it and uncover more information about the financial multiple. Read the page to learn about the financial topics that are relevant to FinAn as well as gain insight into which information FinAn considers to perform a stock evaluation and investment analysis.

This was FinAn!