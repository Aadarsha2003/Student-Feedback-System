from django.shortcuts import render
from django.http import HttpResponseRedirect
import pandas as pd
from io import BytesIO
from django.core.files.base import ContentFile

# Load or create the Excel file to store data
df = pd.DataFrame(columns=['Student Name', 'Class', 'Section', 'Relationship with Guardians', 'Date',
                           'Review from Guardian', 'Review from Interviewer'])

def load_excel_file():
    global df
    try:
        df = pd.read_excel('StudentFeedback.xlsx', engine='openpyxl')
    except FileNotFoundError:
        pass

# Save data to Excel file
def save_to_excel():
    try:
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False)
        writer.save()
        output.seek(0)
        return ContentFile(output.read(), 'feedback.xlsx')
    except Exception as e:
        print(str(e))

# Create your views here.
def feedback_form(request):
    load_excel_file()

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        class_name = request.POST.get('class_name')
        section_name = request.POST.get('section_name')
        relationship = request.POST.get('relationship')
        date = request.POST.get('date')
        guardian_review = request.POST.get('guardian_review')
        interviewer_review = request.POST.get('interviewer_review')

        data = {
            'Student Name': student_name,
            'Class': class_name,
            'Section': section_name,
            'Relationship with Guardians': relationship,
            'Date': date,
            'Review from Guardian': guardian_review,
            'Review from Interviewer': interviewer_review,
        }

        global df
        df = df.append(data, ignore_index=True)
        excel_file = save_to_excel()

        return render(request, 'feedback/thankyou.html', {'excel_file': excel_file})

    return render(request, 'feedback/feedback_form.html')
