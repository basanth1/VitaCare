import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("static/Medicine_Details_With_Price.csv")

df = load_data()

# Initialize session state for cart
if "cart" not in st.session_state:
    st.session_state.cart = {}
    
# Load from prescription session state
prescription = st.session_state.get("prescription_data", {})
medicines = prescription.get("medications", []) if prescription else []

# Add recommended items to cart
def auto_add_medication_to_cart(med):
    matches = df[df["Medicine Name"].str.contains(med["name"], case=False, na=False)]
    if not matches.empty:
        row = matches.iloc[0]
        name = row["Medicine Name"]
        if name not in st.session_state.cart:
            st.session_state.cart[name] = {
                "qty": 1,
                "price": float(row["Price"]),
                "image": row["Image URL"]
            }

# Auto-add prescription meds
for med in medicines:
    auto_add_medication_to_cart(med)
# Add item to cart
def add_to_cart(med):
    name = med['Medicine Name']
    if name in st.session_state.cart:
        st.session_state.cart[name]["qty"] += 1
    else:
        st.session_state.cart[name] = {
            "qty": 1,
            "price": float(med["Price"]),
            "image": med["Image URL"]
        }

# Adjust quantity
def adjust_qty(name, delta):
    if name in st.session_state.cart:
        st.session_state.cart[name]["qty"] += delta
        if st.session_state.cart[name]["qty"] <= 0:
            del st.session_state.cart[name]

# Render a medicine card with a unique key
def render_medicine_card(med, index):
    unique_id = f"{index}_{med['Medicine Name']}".replace(" ", "_")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(med['Image URL'], width=100)
    with col2:
        st.markdown(f"**{med['Medicine Name']}**")
        st.markdown(f"💸 Price: ₹{med['Price']}")
        st.markdown(f"🏭 Manufacturer: {med['Manufacturer']}")
        st.markdown(f"🧪 Composition: {med['Composition']}")
        st.button("Add to Cart", key=f"add_{unique_id}", on_click=add_to_cart, args=[med])
    st.markdown("---")

# Sidebar: Cart display and controls
with st.sidebar:
    st.header("🛒 Your Cart")
    total = 0
    if st.session_state.cart:
        for i, (name, item) in enumerate(st.session_state.cart.items()):
            uid = f"{i}_{name}".replace(" ", "_")
            st.image(item["image"], width=60)
            st.markdown(f"**{name}**")
            st.markdown(f"Price: ₹{item['price']}  | Qty: {item['qty']}")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.button("➖", key=f"minus_{uid}", on_click=adjust_qty, args=[name, -1])
            with col2:
                st.button("➕", key=f"plus_{uid}", on_click=adjust_qty, args=[name, 1])
            total += item["qty"] * item["price"]
            st.markdown("---")
        st.markdown(f"### 🧾 Total: ₹{total}")
        if st.button("Clear Cart"):
            st.session_state.cart.clear()
        if st.button("Proceed to Payment"):
            st.session_state.show_payment = True
    else:
        st.write("Cart is empty.")

# Dummy payment section
if "show_payment" in st.session_state and st.session_state.show_payment:
    st.subheader("💳 Payment")
    name = st.text_input("Full Name")
    address = st.text_area("Delivery Address")
    card = st.text_input("Card Number", max_chars=16)
    if st.button("Pay Now"):
        if name and address and card:
            st.success("✅ Payment Successful! Order Placed.")
            st.session_state.cart.clear()
            st.session_state.show_payment = False
        else:
            st.error("❗ Please fill all fields.")

# Main display
search = st.text_input("🔍 Search Medicine")
max_display = 200
top_meds = df.head(max_display)

if search:
    found = df[df['Medicine Name'].str.contains(search, case=False, na=False)]
    match_in_top = top_meds[top_meds['Medicine Name'].str.contains(search, case=False, na=False)]

    if not found.empty:
        if not match_in_top.empty:
            st.subheader(f"Found in top {max_display} medicines:")
            for i, row in match_in_top.iterrows():
                render_medicine_card(row, i)
        else:
            st.subheader("Found medicine (not in top 200):")
            render_medicine_card(found.iloc[0], 9999)
    else:
        st.error("❌ Medicine not available")
else:
    st.subheader(f"Showing top {max_display} medicines:")
    for i, row in top_meds.iterrows():
        render_medicine_card(row, i)
