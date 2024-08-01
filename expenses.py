from datetime import datetime
import calendar
from flask import Flask, render_template, request, send_from_directory
import mysql.connector
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

app = Flask(__name__)
my_db = mysql.connector.connect(user='root', password='Root', host='127.0.0.1', database="Daily_Expenses")

my_cursor = my_db.cursor()


def insert_data(date, category, item, amount):
    today_date = datetime.now().date()
    sql = "INSERT INTO expenses (date_added, date, category, item, amount) VALUES (%s, %s, %s, %s, %s)"
    val = (today_date, date, category, item, amount)
    my_cursor.execute(sql, val)
    my_db.commit()


def pdf_creator(data, total, month, month_name=None, start=None, end=None):
    def draw_border(canvas, doc):
        width, height = A4  # Page size
        margin = 0.3 * inch  # Margin size

        # Draw a rectangle for the border
        canvas.saveState()
        canvas.setLineWidth(1)
        canvas.setStrokeColorRGB(0, 0, 0)  # Black color
        canvas.rect(margin, margin, width - 2 * margin, height - 2 * margin)
        canvas.restoreState()

    page_margin = 0.5 * inch

    pdf = SimpleDocTemplate(f"monthly.pdf", pagesize=A4, leftMargin=page_margin, rightMargin=page_margin,
                            topMargin=page_margin, bottomMargin=page_margin)
    elements = []

    image = Image('static/logo.png')
    elements.append(image)
    elements.append(Spacer(1, 8))

    styles = getSampleStyleSheet()
    custom_heading_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        leading=20,
        alignment=1  # Center alignment
    )
    # Add heading
    heading = Paragraph(f"{Image('static/logo.png')}Expense Report", custom_heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 8))

    custom_period_style = ParagraphStyle(
        'CustomPeriod1',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        alignment=1  # Center alignment
    )

    if month == "custom":
        period = Paragraph(f"Custom Period: {start} - {end}", custom_period_style)
        elements.append(period)
        elements.append(Spacer(1, 10))
    else:
        period = Paragraph(f"Month: {month_name}", custom_period_style)
        elements.append(period)
        elements.append(Spacer(1, 10))

    # Data for the table
    table_data = [('Date', 'Category', 'Item', 'Amount')] + data + [('', '', 'Total: ', f'{total}')]

    # Create a Table
    table = Table(table_data)

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (2, -1), (2, -1), 'RIGHT'),
        ('BACKGROUND', (-2, -1), (-1, -1), colors.green),
        ('TEXTCOLOR', (-2, -1), (-1, -1), colors.white),
        ('FONTNAME', (-2, -1), (-1, -1), 'Times-Bold'),
    ])

    table.setStyle(style)

    # Add table to the elements
    elements.append(table)

    # Build the PDF
    pdf.build(elements, onFirstPage=draw_border, onLaterPages=draw_border)


@app.route("/", methods=["POST", "GET"])
def expenses():
    today = datetime.now().date()

    save = request.form.get("save")
    this_month_b = request.form.get("this_month")
    last_month_b = request.form.get("last_month")
    custom_b = request.form.get("custom")

    if request.method == "POST":
        if save is not None:
            date = request.form['date']
            category = request.form["expense_category"]
            item = request.form["expense_item"]
            amount = request.form["amount"]

            insert_data(date, category, item, amount)

            my_cursor.execute(f"SELECT COUNT(*) from expenses where date_added='{today}'")
            row_count = my_cursor.fetchone()[0]

            my_cursor.execute(f"select date, category, item, amount from expenses where date_added='{today}'")
            my_result = my_cursor.fetchall()
            rows = [row for row in my_result]

            total = 0
            for count in range(row_count):
                total += rows[count][3]

            return render_template("daily_expenses.html", added=True, details=True, data=rows, row_count=row_count,
                                   total=total)

        elif this_month_b is not None:
            first_of_month = f"{datetime.now().year}-{datetime.now().month}-01"

            my_cursor.execute(f"select date, category, item, amount from expenses where date>'{first_of_month}' "
                              f"and date<'{today}' order by date ASC")
            my_result = my_cursor.fetchall()
            this_month_expenses = [data for data in my_result]

            my_cursor.execute(f"SELECT COUNT(*) from expenses where date>'{first_of_month}' and date<'{today}'")
            row_count = my_cursor.fetchone()[0]

            total = 0
            for count in range(row_count):
                total += this_month_expenses[count][3]

            month_name = calendar.month_name[datetime.now().month]

            pdf_creator(this_month_expenses, total, "this", month_name)
            return render_template('daily_expenses.html')

        elif last_month_b is not None:
            last_month = datetime.now().month - 1
            first_of_last_month = f"{datetime.now().year}-{last_month}-01"
            last_month_end = f"{datetime.now().year}-{last_month}-" \
                             f"{calendar.monthrange(datetime.now().year, last_month)[1]}"

            my_cursor.execute(f"select date, category, item, amount from expenses where "
                              f"date>'{first_of_last_month}' and date<'{last_month_end}' order by date ASC")
            my_result = my_cursor.fetchall()
            last_month_expenses = [data for data in my_result]

            my_cursor.execute(f"SELECT COUNT(*) from expenses where date>'{first_of_last_month}' "
                              f"and date<'{last_month_end}'")
            row_count = my_cursor.fetchone()[0]

            total = 0
            for count in range(row_count):
                total += last_month_expenses[count][3]

            month_name = calendar.month_name[last_month]

            pdf_creator(last_month_expenses, total, "last", month_name)
            return render_template('daily_expenses.html')

        elif custom_b is not None:
            start = request.form['start']
            end = request.form['end']

            my_cursor.execute(f"select date, category, item, amount from expenses where date>'{start}' and "
                              f"date<'{end}' order by date ASC")
            my_result = my_cursor.fetchall()
            custom_expenses = [data for data in my_result]

            my_cursor.execute(f"SELECT COUNT(*) from expenses where date>'{start}' and date<'{end}'")
            row_count = my_cursor.fetchone()[0]

            total = 0
            for count in range(row_count):
                total += custom_expenses[count][3]

            pdf_creator(custom_expenses, total, "custom", start=start, end=end)

    return render_template('daily_expenses.html')


@app.route("/monthly", methods=["POST", "GET"])
def monthly():
    return send_from_directory("", "monthly.pdf")


if __name__ == "__main__":
    app.run(port=9000, debug=True)
