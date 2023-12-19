
    

"""
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    
    if request.method == "POST":
        # Ensure username was submitted
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must provide a number", 400)

        if not symbol:
            return apology("must provide a symbol", 400)
        elif shares < 1:
            return apology("Number must be greater than zero", 400)

        quotes = lookup(symbol)
        if not quotes:
            return apology("Results not found", 400)
        current_price = quotes["price"]
        user_id = session["user_id"]
        amount_required = current_price * shares
        user_cash = db.execute("SELECT cash FROM users WHERE id=?;", user_id)[0]["cash"]
        if user_cash < amount_required:
            return apology("Insufficient Balance", 400)

        user_stocks = None
        try:
            user_stocks = db.execute(
                "SELECT share_no FROM user_stocks where user_id=? AND symbol=?;",
                user_id,
                symbol,
            )[0]["share_no"]
        except:
            pass

        if user_stocks:
            current_no = user_stocks + shares
            stock_update = db.execute(
                "UPDATE user_stocks SET share_no = ? WHERE user_id = ? AND symbol=?;",
                current_no,
                user_id,
                symbol,
            )
        else:
            stock_update = db.execute(
                "INSERT INTO user_stocks (user_id,symbol,share_no) VALUES (?,?,?);",
                user_id,
                symbol,
                shares,
            )
        balance_cash = user_cash - amount_required
        user_update = db.execute(
            "UPDATE users SET cash = ? WHERE id = ?;", balance_cash, user_id
        )
        if not user_update or not stock_update:
            return apology("User update Failed", 403)
        purchase = db.execute(
            "INSERT INTO order_history (user_id,symbol,share_no,purchase_price,purchased_on,action) VALUES (?,?,?,?,?,?);",
            user_id,
            symbol,
            shares,
            current_price,
            datetime.now().strftime("%c"),
            "BUY",
        )
        if not purchase:
            return apology("Purchase Failed", 403)
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
 
    history = db.execute(
        "SELECT symbol,share_no,purchase_price,purchased_on,action FROM order_history WHERE user_id=?",
        session["user_id"],
    )

    return render_template("history.html", orders=history)

"""

"""

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    

    if request.method == "POST":
        # Ensure username was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide a symbol", 400)
        quotes = lookup(symbol)

        if not quotes:
            return apology("Results not found", 400)
        return render_template("quoted.html", quote=quotes)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    
    users = db.execute("SELECT username FROM users;")
    usernames = [user["username"] for user in users]

    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        elif username in usernames:
            return apology("username already exists", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must confirm password", 400)
        elif not password == confirmation:
            return apology("Passwords does not match", 400)

        hashed_pass = generate_password_hash(password)
        success = db.execute(
            "INSERT INTO users (username,hash) VALUES (?,?)", username, hashed_pass
        )
        if success:
            return redirect("/login")
        else:
            return apology("Registration Failed", 403)

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    
    user_id = session["user_id"]
    stock = db.execute("SELECT symbol FROM user_stocks WHERE user_id=?;", user_id)
    stocks = [item["symbol"] for item in stock]
    if request.method == "POST":
        # Ensure username was submitted
        symbol = request.form.get("symbol")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must provide a number", 400)

        if not symbol:
            return apology("must provide a symbol", 400)
        elif symbol not in stocks:
            return apology("Currently not available at Users Account", 400)
        elif shares < 1:
            return apology("Number must be greater than zero", 400)

        quotes = lookup(symbol)
        if not quotes:
            return apology("Results not found", 400)
        current_price = quotes["price"]
        user_id = session["user_id"]
        user_share = db.execute(
            "SELECT share_no FROM user_stocks WHERE user_id=? AND symbol=?;",
            user_id,
            symbol,
        )[0]["share_no"]

        if user_share < shares:
            return apology("Insufficient Stocks", 400)
        user_cash = db.execute("SELECT cash FROM users WHERE id=?;", user_id)[0]["cash"]
        amount_received = current_price * shares
        balance_cash = user_cash + amount_received
        if user_share:
            current_no = user_share - shares
            stock_update = db.execute(
                "UPDATE user_stocks SET share_no = ? WHERE user_id = ? AND symbol=?;",
                current_no,
                user_id,
                symbol,
            )
        if stock_update:
            user_update = db.execute(
                "UPDATE users SET cash = ? WHERE id = ?;", balance_cash, user_id
            )
        if not user_update:
            return apology("User update Failed", 400)
        sell = db.execute(
            "INSERT INTO order_history (user_id,symbol,share_no,purchase_price,purchased_on,action) VALUES (?,?,?,?,?,?);",
            user_id,
            symbol,
            shares,
            current_price,
            datetime.now().strftime("%c"),
            "SELL",
        )
        if not sell:
            return apology("Sell Failed", 400)
        return redirect("/")

    return render_template("sell.html", stocks=stocks)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    print(generate_password_hash("harry"))
    user_id = session["user_id"]
    user = db.execute("SELECT username,cash FROM users WHERE id=?", user_id)[0]
    return render_template("profile.html", user=user)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    user_id = session["user_id"]
    if request.method == "POST":
        try:
            cash = int(request.form.get("cash"))
        except:
            return apology("must provide a number", 400)
        if cash < 1:
            return apology("must provide a positive number", 400)

        user_cash = db.execute("SELECT cash FROM users WHERE id=?;", user_id)[0]["cash"]
        balance_cash = user_cash + cash
        user_update = db.execute(
            "UPDATE users SET cash = ? WHERE id = ?;", balance_cash, user_id
        )
        if user_update:
            return redirect("/profile")
        else:
            return apology("Adding Cash Failed", 400)

    return render_template("Add_cash.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    user_id = session["user_id"]
    if request.method == "POST":
        # Ensure username was submitted
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        prev_pass_hash = db.execute("SELECT hash FROM users WHERE id=?", user_id)[0][
            "hash"
        ]
        print(prev_pass_hash)
        print(generate_password_hash("harry"))
        # Ensure password was submitted
        if not current_password:
            return apology("must provide current password", 400)
        elif not check_password_hash(prev_pass_hash, current_password):
            return apology("current password does not match", 400)

        elif not new_password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must confirm password", 400)
        elif not new_password == confirmation:
            return apology("Passwords does not match", 400)

        hashed_pass = generate_password_hash(new_password)
        success = db.execute(
            "UPDATE users SET hash = ? WHERE id = ?;", hashed_pass, user_id
        )
        if success:
            return redirect("/profile")
        else:
            return apology("Password Change Failed", 400)

    return render_template("change_password.html")
"""