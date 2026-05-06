from io import BytesIO

import qrcode
from django.http import FileResponse
from django.urls import reverse
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .models import Registration


def build_registration_slip(student, semester, request):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    verify_url = request.build_absolute_uri(reverse("registration_slip") + f"?semester={semester}")
    qr_image = qrcode.make(verify_url)
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(60, height - 70, "University Course Registration Slip")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(60, height - 105, f"Name: {student.full_name}")
    pdf.drawString(60, height - 125, f"Reg Number: {student.reg_number}")
    pdf.drawString(60, height - 145, f"Programme: {student.programme}")
    pdf.drawString(60, height - 165, f"Semester: {semester}")
    pdf.drawImage(ImageReader(qr_buffer), width - 150, height - 155, 90, 90)

    y = height - 220
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(60, y, "Code")
    pdf.drawString(130, y, "Course")
    pdf.drawString(390, y, "Credits")
    pdf.drawString(455, y, "Status")
    pdf.setFont("Helvetica", 10)

    for registration in Registration.objects.filter(student=student, semester=semester).select_related("course"):
        y -= 22
        pdf.drawString(60, y, registration.course.code)
        pdf.drawString(130, y, registration.course.title[:42])
        pdf.drawString(405, y, str(registration.course.credit_units))
        pdf.drawString(455, y, registration.status)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{student.reg_number}-{semester}-slip.pdf")
