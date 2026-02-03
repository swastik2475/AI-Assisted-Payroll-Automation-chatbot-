from fastapi import APIRouter, Depends, HTTPException
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os


# import from your backend file (jwt.py)
from jwt import df, get_current_employee

router = APIRouter()


@router.get("/me/payslip-pdf")
def generate_payslip_pdf(emp_id: str = Depends(get_current_employee)):

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

    os.makedirs("payslips", exist_ok=True)
    file_path = f"payslips/{emp_id}_payslip.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "Enlaz PVT LTD")
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, "PAY SLIP")
    y -= 40

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Employee Name : {emp['name']}")
    y -= 20
    c.drawString(50, y, f"Employee ID   : {emp['employee_id']}")
    y -= 20
    c.drawString(50, y, f"Role          : {emp['role']}")
    y -= 20
    c.drawString(50, y, f"Pay Type      : {emp['pay_type']}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "EARNINGS")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(70, y, f"Gross Salary  : ₹ {gross_salary:.2f}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "DEDUCTIONS")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(70, y, f"PF / Tax      : ₹ {deductions:.2f}")
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"NET PAY : ₹ {net_pay:.2f}")
    y -= 40

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, y, "This is a system generated payslip.")

    c.save()

    return {
        "message": "Payslip PDF generated successfully",
        "file_path": file_path
    }
