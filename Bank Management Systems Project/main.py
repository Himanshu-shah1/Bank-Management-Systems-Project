import streamlit as st
import pickle
import os
import pathlib

# ---------------- CLASS ---------------- #
class Account:
    def __init__(self, accNo, name, acc_type, deposit):
        self.accNo = accNo
        self.name = name
        self.type = acc_type
        self.deposit = deposit

# ---------------- FILE HANDLING ---------------- #
FILE_NAME = "accounts.data"

def load_accounts():
    if pathlib.Path(FILE_NAME).exists():
        with open(FILE_NAME, 'rb') as f:
            return pickle.load(f)
    return []

def save_accounts(accounts):
    with open(FILE_NAME, 'wb') as f:
        pickle.dump(accounts, f)

# ---------------- FUNCTIONS ---------------- #
def create_account(accNo, name, acc_type, deposit):
    accounts = load_accounts()
    accounts.append(Account(accNo, name, acc_type, deposit))
    save_accounts(accounts)

def get_account(accNo):
    accounts = load_accounts()
    for acc in accounts:
        if acc.accNo == accNo:
            return acc
    return None

def update_accounts(updated_accounts):
    save_accounts(updated_accounts)

# ---------------- UI ---------------- #
st.title("🏦 Bank Management System")
st.markdown("### 👨‍💻 Project Created by **Himanshu Shah**")

# Sidebar credit
st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Himanshu Shah**")

menu = st.sidebar.selectbox("Menu", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Balance Enquiry",
    "All Accounts",
    "Delete Account",
    "Modify Account"
])

# ---------------- CREATE ---------------- #
if menu == "Create Account":
    st.header("Create New Account")
    accNo = st.number_input("Account Number", step=1)
    name = st.text_input("Account Holder Name")
    acc_type = st.selectbox("Account Type", ["Saving", "Current"])
    deposit = st.number_input("Initial Deposit", step=100)

    if st.button("Create"):
        create_account(accNo, name, acc_type, deposit)
        st.success("Account Created Successfully!")

# ---------------- DEPOSIT ---------------- #
elif menu == "Deposit":
    st.header("Deposit Amount")
    accNo = st.number_input("Account Number", step=1)
    amount = st.number_input("Amount", step=100)

    if st.button("Deposit"):
        accounts = load_accounts()
        for acc in accounts:
            if acc.accNo == accNo:
                acc.deposit += amount
                update_accounts(accounts)
                st.success("Amount Deposited!")
                break

# ---------------- WITHDRAW ---------------- #
elif menu == "Withdraw":
    st.header("Withdraw Amount")
    accNo = st.number_input("Account Number", step=1)
    amount = st.number_input("Amount", step=100)

    if st.button("Withdraw"):
        accounts = load_accounts()
        for acc in accounts:
            if acc.accNo == accNo:
                if acc.deposit >= amount:
                    acc.deposit -= amount
                    update_accounts(accounts)
                    st.success("Amount Withdrawn!")
                else:
                    st.error("Insufficient Balance")
                break

# ---------------- BALANCE ---------------- #
elif menu == "Balance Enquiry":
    st.header("Balance Enquiry")
    accNo = st.number_input("Account Number", step=1)

    if st.button("Check Balance"):
        acc = get_account(accNo)
        if acc:
            st.info(f"Balance: ₹{acc.deposit}")
        else:
            st.error("Account Not Found")

# ---------------- ALL ACCOUNTS ---------------- #
elif menu == "All Accounts":
    st.header("All Account Holders")
    accounts = load_accounts()
    if accounts:
        data = [{
            "Acc No": acc.accNo,
            "Name": acc.name,
            "Type": acc.type,
            "Balance": acc.deposit
        } for acc in accounts]
        st.table(data)
    else:
        st.warning("No accounts found")

# ---------------- DELETE ---------------- #
elif menu == "Delete Account":
    st.header("Delete Account")
    accNo = st.number_input("Account Number", step=1)

    if st.button("Delete"):
        accounts = load_accounts()
        accounts = [acc for acc in accounts if acc.accNo != accNo]
        update_accounts(accounts)
        st.success("Account Deleted")

# ---------------- MODIFY ---------------- #
elif menu == "Modify Account":
    st.header("Modify Account")
    accNo = st.number_input("Account Number", step=1)

    acc = get_account(accNo)
    if acc:
        name = st.text_input("Name", value=acc.name)
        acc_type = st.selectbox("Type", ["Saving", "Current"], index=0 if acc.type=="Saving" else 1)
        deposit = st.number_input("Balance", value=acc.deposit)

        if st.button("Update"):
            accounts = load_accounts()
            for a in accounts:
                if a.accNo == accNo:
                    a.name = name
                    a.type = acc_type
                    a.deposit = deposit
            update_accounts(accounts)
            st.success("Account Updated")
    else:
        st.warning("Enter valid account number")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.markdown(
    "<center>👨‍💻 Project Created by <b>Himanshu Shah</b></center>",
    unsafe_allow_html=True
)
