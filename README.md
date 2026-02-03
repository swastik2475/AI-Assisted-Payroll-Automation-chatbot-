# AI-Assisted-Payroll-Automation-chatbot-
Payroll Automation System
Rule-Based Payroll with API-Driven Design

Overview

This project is a rule-based payroll automation system built for ABC Company to simplify payroll processing and reduce manual HR effort. The system uses secure APIs and predefined payroll rules to calculate salaries accurately while maintaining transparency and compliance.

An AI-powered assistant is integrated only for explanation and support, allowing employees to understand their payroll details without modifying any calculations.

API Documentation (Swagger Preview)

The above image shows the available authentication, employee self-service, and payroll-related APIs exposed by the system.

Key Features

Secure authentication system

Employee self-service payroll access

Rule-based payroll calculation

Attendance-based salary processing

Payslip generation in PDF format

Transparent and auditable payroll logic

AI support for payroll explanation (read-only)

System Design

Backend APIs handle authentication, data validation, attendance, and payroll

Rule Engine applies salary, leave, and deduction rules

Database stores employee, attendance, and payroll data

AI Assistant explains payroll outcomes without altering data

API Endpoints
Authentication

POST /login
Authenticates the user and returns an access token.

Employee Self-Service (Authenticated)

All endpoints below require a valid authentication token.

GET /me/profile
Retrieve the logged-in employee’s profile details.

GET /me/attendance
Fetch attendance records for the logged-in employee.

GET /me/validate
Validate employee data before payroll calculation.

Payroll

GET /me/payroll
Calculate payroll for the logged-in employee using predefined rule-based logic.

GET /me/payslip-pdf
Generate and download the employee’s payslip in PDF format.

Payroll Flow

User logs in and receives an authentication token

Employee profile and attendance data are fetched

Data is validated using payroll rules

Payroll is calculated using rule-based logic

Payslip is generated and provided as a PDF

Employees can request payroll explanations via AI support

Why Rule-Based Payroll?

Ensures accuracy and compliance
Easy to audit and debug
Prevents incorrect AI-driven decisions
Builds trust between employees and HR teams
Security & Compliance
Token-based authentication
Protected employee endpoints

AI has no permission to modify payroll data

Disclaimer

AI is used strictly for explanation and support. All payroll calculations are rule-based and controlled by backend logic.
