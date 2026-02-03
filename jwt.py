from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

SECRET_KEY = "payroll-secret-key"
ALGORITHM = "HS256"

security = HTTPBearer()

# load dummy employee data
df = pd.read_csv(
    r"C:\Users\BIT\OneDrive\Desktop\intern\employee_payroll_dummy.csv"
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(data: LoginRequest):
    user = df[
        (df["username"] == data.username) &
        (df["password"] == data.password)
    ]

    if user.empty:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    emp_id = user.iloc[0]["employee_id"]

    token = jwt.encode(
        {"emp_id": emp_id},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_employee(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload["emp_id"]

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@app.get("/me/profile")
def my_profile(emp_id: str = Depends(get_current_employee)):
    emp = df[df["employee_id"] == emp_id]

    if emp.empty:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp = emp.iloc[0]

    return {
        "employee_id": emp["employee_id"],
        "name": emp["name"],
        "role": emp["role"],
        "pay_type": emp["pay_type"]
    }


@app.get("/me/attendance")
def my_attendance(emp_id: str = Depends(get_current_employee)):
    emp = df[df["employee_id"] == emp_id]

    if emp.empty:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp = emp.iloc[0]

    return {
        "working_days": int(emp["working_days"]),
        "leaves": int(emp["leaves"])
    }


@app.get("/me/validate")
def validate_my_data(emp_id: str = Depends(get_current_employee)):
    emp = df[df["employee_id"] == emp_id]

    if emp.empty:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp = emp.iloc[0]
    issues = []

    if emp["working_days"] < 0:
        issues.append("Working days cannot be negative")

    if emp["working_days"] > 26:
        issues.append("Working days exceed monthly limit")

    if emp["leaves"] < 0:
        issues.append("Leaves cannot be negative")

    if emp["leaves"] > emp["working_days"]:
        issues.append("Leaves cannot exceed working days")

    if emp["pay_type"] not in ["monthly", "hourly"]:
        issues.append("Invalid pay type")

    if issues:
        return {
            "status": "INVALID",
            "issues": issues
        }

    return {
        "status": "VALID",
        "message": "Attendance and payroll data is valid"
    }


@app.get("/me/payroll")
def calculate_my_payroll(emp_id: str = Depends(get_current_employee)):
    emp = df[df["employee_id"] == emp_id]

    if emp.empty:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp = emp.iloc[0]

    if emp["pay_type"] == "monthly":
        per_day_salary = emp["rate"] / 22
        gross_salary = per_day_salary * emp["working_days"]
        deductions = gross_salary * 0.05
    else:
        gross_salary = emp["working_days"] * 8 * emp["rate"]
        deductions = 0

    net_pay = gross_salary - deductions

    return {
        "pay_type": emp["pay_type"],
        "gross_salary": round(gross_salary, 2),
        "deductions": round(deductions, 2),
        "net_pay": round(net_pay, 2)
    }


from payslip import router as payslip_router
app.include_router(payslip_router)
