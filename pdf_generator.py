"""
Generates a fee voucher PDF containing TWO copies on one A4 page:
  - Top half:    OFFICE COPY
  - Bottom half: STUDENT COPY
Built with reportlab only (no external binaries required).
"""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def _draw_slip(c, x, y, width, height, payment, student, dev, college_name, copy_label):
    """Draw a single voucher slip with its top-left corner at (x, y - height)."""
    top = y
    left = x
    right = x + width

    # Outer border
    c.setLineWidth(1.2)
    c.rect(left, top - height, width, height)

    cursor = top - 8 * mm

    # Copy label (top right, small)
    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(right - 4 * mm, top - 5 * mm, copy_label)

    # Header
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(left + width / 2, cursor, college_name)
    cursor -= 5 * mm
    c.setFont("Helvetica", 7)
    c.drawCentredString(left + width / 2, cursor, "(Approved by HEC / Affiliated with University)")
    cursor -= 3 * mm
    c.setLineWidth(0.8)
    c.line(left + 4 * mm, cursor, right - 4 * mm, cursor)
    cursor -= 5 * mm

    # Meta row: date / candidate no
    c.setFont("Helvetica", 8)
    today_str = payment["due_date"] or ""
    c.drawString(left + 4 * mm, cursor, f"Date: {payment['due_date'] or '-'}")
    c.drawRightString(right - 4 * mm, cursor, f"Candidate No: {student['candidate_no'] or '-'}")
    cursor -= 5 * mm

    # Student info
    c.setFont("Helvetica-Bold", 8)
    c.drawString(left + 4 * mm, cursor, f"Student Name: {student['name']}")
    cursor -= 4.5 * mm
    c.drawString(left + 4 * mm, cursor, f"Father Name: {student['father_name'] or '-'}")
    cursor -= 4.5 * mm
    course_line = f"Program: {student['course_name'] or '-'}   |   Duration: {student['course_duration'] or '-'}"
    c.drawString(left + 4 * mm, cursor, course_line)
    cursor -= 6 * mm

    # Table
    col_widths = [12 * mm, width - 12 * mm - 30 * mm - 8 * mm, 30 * mm]
    row_h = 6 * mm
    table_top = cursor
    table_left = left + 4 * mm

    rows = [
        ("S.No", "Particulars", "Amount (Rs.)"),
        ("1", "ID Card Fee", f"{payment['id_card_fee']:.0f}" if payment["id_card_fee"] else "---"),
        ("2", f"Tuition Fee (Installment {payment['installment_no']} of {student['installment_count']})",
         f"{payment['tuition_amount']:.0f}"),
        ("3", "DMC", f"{payment['dmc_fee']:.0f}" if payment["dmc_fee"] else "---"),
        ("4", "Exam Fee", f"{payment['exam_fee']:.0f}" if payment["exam_fee"] else "---"),
        ("5", "Fund Fee", f"{payment['fund_fee']:.0f}" if payment["fund_fee"] else "---"),
    ]
    total = (payment["tuition_amount"] + payment["id_card_fee"] + payment["dmc_fee"]
             + payment["exam_fee"] + payment["fund_fee"])
    rows.append(("6", "Total", f"{total:.0f}"))

    c.setLineWidth(0.7)
    y_cursor = table_top
    for i, row in enumerate(rows):
        is_header = i == 0
        is_total = i == len(rows) - 1
        # row background for header
        if is_header:
            c.setFillColor(colors.whitesmoke)
            c.rect(table_left, y_cursor - row_h, sum(col_widths), row_h, fill=1, stroke=0)
            c.setFillColor(colors.black)

        xpos = table_left
        c.setFont("Helvetica-Bold" if (is_header or is_total) else "Helvetica", 7.5)
        for ci, (text, cw) in enumerate(zip(row, col_widths)):
            c.rect(xpos, y_cursor - row_h, cw, row_h, fill=0, stroke=1)
            if ci == 1:
                c.drawString(xpos + 1.5 * mm, y_cursor - row_h + 2 * mm, str(text)[:48])
            else:
                c.drawCentredString(xpos + cw / 2, y_cursor - row_h + 2 * mm, str(text))
            xpos += cw
        y_cursor -= row_h

    cursor = y_cursor - 5 * mm

    # Footer info
    c.setFont("Helvetica", 7.5)
    paid_status = "PAID" if payment["paid"] else "UNPAID"
    c.drawString(left + 4 * mm, cursor,
                 f"Installment: {payment['installment_no']} of {student['installment_count']}   "
                 f"Status: {paid_status}")
    c.drawRightString(right - 4 * mm, cursor, f"Due Date: {payment['due_date'] or '-'}")
    cursor -= 8 * mm

    # Signature area
    c.setLineWidth(0.6)
    c.line(left + 8 * mm, cursor, left + 38 * mm, cursor)
    c.line(right - 38 * mm, cursor, right - 8 * mm, cursor)
    cursor -= 3 * mm
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(left + 23 * mm, cursor, "Student Sign")
    c.drawCentredString(right - 23 * mm, cursor, "Accountant Stamp")
    cursor -= 5 * mm

    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(left + width / 2, cursor, "FEE ONCE PAID WILL NOT BE RETURNED IN ANY CASE")
    cursor -= 4 * mm

    c.setFont("Helvetica-Oblique", 6.5)
    c.drawCentredString(
        left + width / 2, cursor,
        f"Need software like this? Contact {dev['name']} ({dev['title']}) - WhatsApp: {dev['whatsapp_display']}"
    )


def build_voucher_pdf(payment, student, dev, college_name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    page_w, page_h = A4

    margin = 10 * mm
    slip_w = page_w - 2 * margin
    slip_h = (page_h - 3 * margin) / 2

    # Office copy (top)
    _draw_slip(c, margin, page_h - margin, slip_w, slip_h, payment, student, dev, college_name, "OFFICE COPY")
    # dashed cut line
    c.setDash(3, 3)
    c.setLineWidth(0.5)
    mid_y = page_h - margin - slip_h - (margin / 2)
    c.line(margin, mid_y, page_w - margin, mid_y)
    c.setDash()

    # Student copy (bottom)
    _draw_slip(c, margin, page_h - margin - slip_h - margin, slip_w, slip_h, payment, student, dev, college_name, "STUDENT COPY")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
