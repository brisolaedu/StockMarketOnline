import datetime
import yfinance as yf

# Search Stock
def search_stock(db, user_name, stock_name, number):
    
    # Retrieve Stock's Price
    stock = yf.Ticker(stock_name)
    ticker = stock.history(period='1d')

    try:
        price = ticker['Close'].iloc[0]

    except IndexError:
        return

    buy_stock(user_name, price, stock_name, number, db)
 

def buy_stock(user_name, price, stock_name, number, db):
    db.execute("INSERT INTO accounts (person_id, stock_name, stock_price, shares_bought, time_bought) VALUES (?, ?, ?, ?, ?)", user_name, stock_name, price, number, datetime.datetime.now())


# Show Portfolio
def portfolio(db, user_name):
    total_value = 0

    stocks = db.execute("SELECT stock_name, shares_bought, stock_price FROM accounts WHERE person_id = ?", user_name)
    #return stocks

    for shares in stocks:
        shares["stock_price"] = f"{float(shares["stock_price"]):.2f}"

        value = float(shares["stock_price"]) * int(shares["shares_bought"])
        total_value += value

    total_value = f"{float(total_value):.2f}"

    return stocks, total_value


# Sell Stocks
def sell_stocks(db, user_name, stock_name, number, stock_index):
    number = int(number)
    shares = db.execute("SELECT * FROM accounts WHERE stock_name = ? AND person_id = ? AND shares_bought >= ?", stock_name, user_name, number)
    if shares == []:
        return

    index = int(stock_index) - 1
    time = shares[index]["time_bought"]
    sell = get_stocks(index, number, stock_name, user_name, db, time)

    return sell


# Get Stocks Confirmation
def get_stocks(index, number, answer, user, db, time):
    number_sh = db.execute("SELECT shares_bought FROM accounts WHERE stock_name = ? AND person_id = ? AND shares_bought >= ?", answer, user, number)
    number_sh = number_sh[index]["shares_bought"]
    new_number = number_sh - number
    db.execute("UPDATE accounts SET shares_bought = ? WHERE stock_name = ? AND person_id = ? AND time_bought = ?", new_number, answer, user, time)

    price = db.execute("SELECT stock_price FROM accounts WHERE stock_name = ? AND person_id = ? AND shares_bought = ? and time_bought = ?", answer, user, new_number, time)
    sell = float(price[0]["stock_price"]) * number
    sell = f"{float(sell):.2f}"

    if new_number == 0:
        db.execute("DELETE FROM accounts WHERE shares_bought = 0;")

    return sell
