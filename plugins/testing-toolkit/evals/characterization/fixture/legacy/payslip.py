import datetime
import uuid


def render_payslip(employee, hours, rate):
    ref = uuid.uuid4().hex[:8].upper()
    now = datetime.datetime.now()
    overtime = 0
    if hours > 160:
        overtime = hours - 160
        hours = 160
    gross = hours * rate + overtime * rate * 1.5
    if gross > 5000:
        tax = gross * 0.3
    elif gross > 1000:
        tax = gross * 0.2
    else:
        tax = 0
    if employee.get("union"):
        dues = 25
    else:
        dues = 0
    net = gross - tax - dues
    name = employee["name"].upper()
    lines = [
        "PAYSLIP " + ref,
        "Issued " + now.strftime("%Y-%m-%d %H:%M"),
        "Employee: " + name,
        "Gross: %.2f" % gross,
        "Tax: %.2f" % tax,
        "Dues: %.2f" % dues,
        "Net: %.2f" % net,
    ]
    if overtime:
        lines.insert(3, "Overtime hours: %d" % overtime)
    return "\n".join(lines)
