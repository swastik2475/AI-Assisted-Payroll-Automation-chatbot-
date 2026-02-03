import streamlit as st
import requests


API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Payroll Assistant",
    layout="centered"
)



def login_user(username: str, password: str):
    return requests.post(
        f"{API_BASE_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )


def call_api(endpoint: str, token: str):
    return requests.get(
        f"{API_BASE_URL}{endpoint}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


st.session_state.setdefault("token", None)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("payslip_pdf", None)
st.session_state.setdefault("user_name", None)


if st.session_state.token is None:
    st.title("Employee Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password")
        else:
            response = login_user(username, password)

            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]

                # Fetch logged-in user profile once
                profile_res = call_api(
                    "/me/profile",
                    st.session_state.token
                )

                if profile_res.status_code == 200:
                    st.session_state.user_name = (
                        profile_res.json()["name"].lower()
                    )

                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")



else:
    st.title("Payroll Assistant")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.messages.clear()
        st.session_state.payslip_pdf = None
        st.session_state.user_name = None
        st.rerun()


    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about your payroll")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        text = user_input.lower()
        token = st.session_state.token
        reply = "Sorry, I didn’t understand that."


        if "profile" in text:
            res = call_api("/me/profile", token)
            if res.status_code == 200:
                data = res.json()
                reply = (
                    f"**Name:** {data['name']}\n\n"
                    f"**Role:** {data['role']}\n\n"
                    f"**Pay Type:** {data['pay_type']}"
                )


        elif "attendance" in text:
            res = call_api("/me/attendance", token)
            if res.status_code == 200:
                data = res.json()
                reply = (
                    f"**Working Days:** {data['working_days']}\n\n"
                    f"**Leaves:** {data['leaves']}"
                )


        elif "salary" in text or "payroll" in text:
            known_names = ["rahul", "vijay","Anjali ","Vikas","Sneha","Priya","Amit","neha","arjun","kavita"]
            mentioned_name = next(
                (name for name in known_names if name in text),
                None
            )

            if mentioned_name and mentioned_name != st.session_state.user_name:
                reply = (
                    " You are not authorized to view "
                    "another employee’s salary details."
                )
            else:
                res = call_api("/me/payroll", token)
                if res.status_code == 200:
                    data = res.json()
                    reply = (
                        f"**Gross Salary:** ₹{data['gross_salary']}\n\n"
                        f"**Deductions:** ₹{data['deductions']}\n\n"
                        f"**Net Pay:** ₹{data['net_pay']}"
                    )

        elif "validate" in text:
            res = call_api("/me/validate", token)
            if res.status_code == 200:
                data = res.json()
                reply = (
                    " Your data is valid."
                    if data["status"] == "VALID"
                    else " Issues:\n" + "\n".join(data["issues"])
                )

    
        elif "payslip" in text:
            res = call_api("/me/payslip-pdf", token)
            if res.status_code == 200:
                file_info = res.json()
                with open(file_info["file_path"], "rb") as pdf:
                    st.session_state.payslip_pdf = pdf.read()

                reply = "Payslip generated successfully. You can download it below."

        # -----------------------
        # Fallback
        # -----------------------
        else:
            reply = (
                "You can ask about:\n"
                "- Profile\n"
                "- Attendance\n"
                "- Salary\n"
                "- Validation\n"
                "- Payslip"
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()

    if st.session_state.payslip_pdf:
        st.download_button(
            label="⬇ Download Payslip PDF",
            data=st.session_state.payslip_pdf,
            file_name="payslip.pdf",
            mime="application/pdf"
        )
