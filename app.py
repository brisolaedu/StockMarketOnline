from flask import Flask, request, render_template, redirect, session
from functions import name_confirmation, user_deleter, user_login, user_register, hash_code
from shares import search_stock, portfolio, sell_stocks
from cs50 import SQL


app = Flask(__name__)
db = SQL("sqlite:///static/accounts.db")
app.secret_key = '$abcdef'

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Start Page
@app.route("/", methods=["GET", "POST"])
def start():
    if "login" in request.form:
        return redirect("/login")
    elif "register" in request.form:
        return redirect("/register")
    elif "delete" in request.form:
        return redirect("/deleter")
    else:
        return render_template("start.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "back" in request.form:
            return redirect("/")
        
        name = request.form.get("user").lower().strip()
        password = request.form.get("password").strip()

        if user_login(db, name, password):
            session['username'] = hash_code(name)
            return redirect("/options")
        else:
            return render_template("login.html")
    
    else:
        return render_template("login.html")
    

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if "back" in request.form:
            return redirect("/")
         
        name = request.form.get("user").lower().strip()
        password = request.form.get("password").strip()

        if not name_confirmation(db, name):
            user_register(db, name, password)
            return redirect("/")
        else:
            return render_template("register.html")
    
    else:
        return render_template("register.html")
    

# Delete Page
@app.route("/deleter", methods=["GET", "POST"])
def deleter():
    if request.method == "POST":
        if "back" in request.form:
            return redirect("/")
        
        name = request.form.get("user").lower().strip()
        password = request.form.get("password").strip()

        if user_login(db, name, password):
            user_deleter(db, name, password)
            return redirect("/")
        else:
            return render_template("deleter.html")
    
    else:
        return render_template("deleter.html")
    

# Options Page
@app.route("/options", methods=["GET", "POST"])
def options():
    if "buy" in request.form:
        return redirect("/buy")
    elif "view" in request.form:
        return redirect("/view")
    elif "sell" in request.form:
        return redirect("/sell")
    elif "back" in request.form:
        return redirect("/")
    
    else:
        return render_template("options.html")
    

@app.route("/buy", methods=["GET", "POST"])
def buy():
    if request.method == "POST":
        if "back" in request.form:
            return redirect("/options")
        
        stock = request.form.get("search").strip()
        number = int(request.form.get("number").strip())

        search_stock(db, session['username'], stock, number)

        return redirect("/options")
    else:
        return render_template("buy.html")


@app.route("/view", methods=["GET", "POST"])
def view():
    if request.method == "POST":
        return redirect("/view")
    else:
        stocks, total_value = portfolio(db, session['username'])
        return render_template("portfolio.html", stocks=stocks, total_value=total_value)


@app.route("/sell", methods=["GET", "POST"])
def sell():
    if request.method == "POST":
        if "back" in request.form:
            return redirect("/view")
        
        stock_name = request.form.get("search")
        number = request.form.get("number")
        index = request.form.get("index")

        sell = sell_stocks(db, session['username'], stock_name, number, index)
        return render_template("sell.html", sell=sell)
    else:
        return render_template("sell.html")


if __name__ == "__main__":
    app.run(debug=True)