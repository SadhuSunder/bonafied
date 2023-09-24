from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

# Input validation functions
def validate_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print(f"Invalid input for {prompt}. Please try again.")

def is_valid_name(name):
    return all(char.isalpha() or char == '.' or char.isspace() for char in name)

def is_valid_date(date):
    try:
        return datetime.strptime(date, '%d/%m/%Y') >= datetime(2023, 9, 23)
    except ValueError:
        return False

def is_valid_year(year):
    return year.isdigit() and 1 <= int(year) <= 4

def is_valid_semester(semester):
    return semester.isdigit() and int(semester) in [1, 2]

def is_valid_fathers_name(name):
    return all(char.isalpha() or char == '.' or char.isspace() for char in name)

def is_valid_academic_year(academic_year):
    if len(academic_year) == 7:
        start, end = academic_year.split('-')
        return start.isdigit() and end.isdigit() and len(start) == 4 and len(end) == 2
    return False

def is_valid_branch(branch):
    return branch in ["CSE-AIML", "CSE", "CSE-DS", "CSE-CS"]

# Input validation
name = validate_input("Enter student's name: ", is_valid_name)
roll_number = input("Enter student's roll number: ")
year = validate_input("Enter year (1-4): ", is_valid_year)
semester = validate_input("Enter semester (1 or 2): ", is_valid_semester)
date = validate_input("Enter date (dd/mm/yyyy, e.g., 23/09/2023): ", is_valid_date)
branch = validate_input("Enter branch (CSE-AIML / CSE / CSE-DS / CSE-CS): ", is_valid_branch)
fathers_name = validate_input("Enter father's name: ", is_valid_fathers_name)
academic_year = validate_input("Enter academic year (yyyy-yy, e.g., 2022-23): ", is_valid_academic_year)

# Generate the certificate PDF
doc = SimpleDocTemplate("bonafide_certificate.pdf", pagesize=letter)
styles = getSampleStyleSheet()

# Constants
institution_name = "St. Mary's Group Of Institutions Hyderabad"
logo_path = "logo.png"

# Custom paragraph styles
institution_style = ParagraphStyle(
    name='InstitutionStyle', fontSize=19, textColor=colors.black, alignment=1, fontName='Helvetica-Bold', spaceAfter=6
)
approval_style = ParagraphStyle(name='ApprovalStyle', fontSize=8, spaceBefore=9, leftIndent=70)
date_style = ParagraphStyle(name='DateStyle', fontSize=10, textColor=colors.black, alignment=2)
certificate_style = ParagraphStyle(
    name='CertificateStyle', fontSize=12, textColor=colors.black, alignment=0, spaceBefore=12, spaceAfter=12, fontName='Helvetica-Bold'
)
principal_heading_style = ParagraphStyle(name='PrincipalHeadingStyle', fontSize=10, textColor=colors.black, alignment=2, spaceBefore=50)
main_heading_style = ParagraphStyle(name='MainHeadingStyle', fontSize=15, textColor=colors.black, alignment=1, spaceAfter=4, spaceBefore=12)

# Calculate semester year
year_suffix = "th" if int(year) > 3 else "rd"
semester_suffix = "th" if int(semester) > 3 else "nd"
semester_year = f"{year}{year_suffix} Year - {semester}{semester_suffix} Semester"

# Create a Paragraph for the institution name
institution_paragraph = Paragraph(institution_name, institution_style)

# Create a Table to position the logo, main heading, and date
data = [
    [Image(logo_path, width=100, height=50, kind='proportional', mask='auto'), Paragraph("<u><b>Bonafied Certificate</b></u>", main_heading_style), Paragraph(f"<b>Date: {date}</b>", date_style)],
]

# Adjust the column widths and rowHeights to match the layout
colWidths = [100, 320, 100]
rowHeights = [50]
table = Table(data, colWidths=colWidths, rowHeights=rowHeights)

# Apply TableStyle to align the elements in the first row
table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))

# Create a Paragraph for the approval information and address
approval_paragraph = Paragraph(
    "Approved by AICTE & PCI, Affiliated to JNTUH & SBTET, Permitted by Govt. of T.S<br/>"
    "Deshmukhi Village, Near Ramoji Film City, Behind Mount Opera, Hyderabad - 508284. T.S. INDIA",
    approval_style,
)

# Create a Paragraph for the certificate text
certificate_text = f"""<p>This is to certify that Mr/Miss <u><b>{name}</b></u> S/o,D/o.Sri <u><b>{fathers_name}</b></u> is/was a bonafied student of this college bearing roll number <u><b>{roll_number}</b></u>, Studying/ has studied  <b>{semester_year}</b> of M.tech /B.tech /M.Pharmacy /B.Pharmacy /MBA /MCA /Diploma in the branch of <u><b>{branch}</b></u> for the academic year/years <u><b>{academic_year}</b></u></p>"""

certificate_paragraph = Paragraph(certificate_text, certificate_style)

# Create a Paragraph for the principal heading "Principal"
principal_heading = Paragraph("<b>Principal</b>", principal_heading_style)

# Build the PDF content
content = [institution_paragraph, approval_paragraph, table, certificate_paragraph, principal_heading]

# Build the PDF document
doc.build(content)

print("Bonafide certificate has been generated as 'bonafide_certificate.pdf'")
