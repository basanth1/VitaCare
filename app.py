from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from utils.prescription_parser import get_prescription_informations
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for sessions

# Load medicine data
med_data = pd.read_csv("data/Medicine_Details_With_Price.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/appointment", methods=["GET", "POST"])
def appointment():
    if request.method == "POST":
        name = request.form.get("name")
        contact = request.form.get("contact")
        doctor = request.form.get("doctor")
        date = request.form.get("date")
        time = request.form.get("time")

        if not name or not contact:
            error = "Please enter your name and contact info."
            return render_template("appointment.html", error=error)

        room_name = f"vh_{doctor.replace(' ', '')}_{name.replace(' ', '')}_{int(datetime.now().timestamp())}"
        return render_template("appointment.html", success=True, room_name=room_name)

    return render_template("appointment.html")

@app.route("/prescription", methods=["GET", "POST"])
def prescription():
    if request.method == "POST":
        file = request.files.get("prescription")
        if file:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = file.filename.replace(" ", "_")
            filepath = os.path.join("uploads", f"{ts}_{filename}")
            os.makedirs("uploads", exist_ok=True)
            file.save(filepath)

            result = get_prescription_informations([filepath])
            session["prescription_data"] = result
            os.remove(filepath)  # optional cleanup
            return render_template("prescription.html", result=result)

    return render_template("prescription.html")

@app.route("/orders", methods=["GET", "POST"])
def orders():
    search = request.args.get("search", "")
    cart = session.get("cart", {})

    df = med_data.copy()
    if search:
        df = df[df["Medicine Name"].str.contains(search, case=False, na=False)]

    return render_template("orders.html", medicines=df.head(200).to_dict(orient="records"), cart=cart)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    name = request.form["name"]
    price = float(request.form["price"])
    image = request.form["image"]

    cart = session.get("cart", {})
    if name in cart:
        cart[name]["qty"] += 1
    else:
        cart[name] = {"qty": 1, "price": price, "image": image}
    session["cart"] = cart
    return redirect(url_for("orders"))
@app.route("/update_cart", methods=["POST"])
def update_cart():
    name = request.form["name"]
    action = request.form["action"]
    cart = session.get("cart", {})

    if name in cart:
        if action == "plus":
            cart[name]["qty"] += 1
        elif action == "minus":
            cart[name]["qty"] -= 1
            if cart[name]["qty"] <= 0:
                del cart[name]

    session["cart"] = cart
    return redirect(url_for("orders"))

@app.route("/checkout", methods=["POST"])
def checkout():
    name = request.form.get("name")
    address = request.form.get("address")
    card = request.form.get("card")

    if name and address and card:
        session.pop("cart", None)
        return render_template("orders.html", success="✅ Payment successful! Order placed.", medicines=med_data.head(200).to_dict(orient="records"), cart={})
    else:
        return render_template("orders.html", error="❗ Please fill in all payment details.", medicines=med_data.head(200).to_dict(orient="records"), cart=session.get("cart", {}))

@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("orders"))

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
