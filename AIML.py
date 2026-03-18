import tkinter as tk
from tkinter import messagebox, filedialog
import nltk
import string
import PyPDF2

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

# PDF export
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Global variables for report
current_keywords = []
current_score = 0
current_category = ""

# 🔹 Preprocess text
def preprocess(text):
    text = text.lower()
    words = wordpunct_tokenize(text)

    filtered = []
    for w in words:
        if w not in stopwords.words('english') and w not in string.punctuation:
            filtered.append(w)

    return filtered


# 🔹 Category function
def get_category(keywords):
    categories = []

    if any(skill in keywords for skill in ['html', 'css', 'javascript', 'node', 'express']):
        categories.append("Web Developer")

    if any(skill in keywords for skill in ['machine', 'learning', 'ai']):
        categories.append("AI / ML")

    if any(skill in keywords for skill in ['data', 'analysis', 'python']):
        categories.append("Data Science")

    if any(skill in keywords for skill in ['c', 'c++', 'java', 'dbms', 'os']):
        categories.append("Core CS")

    return ", ".join(categories) if categories else "General"


# 🔹 Read PDF
def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
    except:
        messagebox.showerror("Error", "Could not read PDF!")

    return text


# 🔹 Analyze Resume
def analyze_resume():
    global current_keywords, current_score, current_category

    text = input_text.get("1.0", tk.END)

    if text.strip() == "":
        messagebox.showwarning("Warning", "Enter resume text or upload PDF!")
        return

    words = preprocess(text)

    skills = ['python', 'java', 'c', 'c++', 'javascript', 'html', 'css',
              'sql', 'node', 'express', 'machine', 'learning',
              'data', 'analysis', 'ai']

    keywords = list(set(words) & set(skills))
    score = len(keywords)
    category = get_category(keywords)

    # Store globally for export
    current_keywords = keywords
    current_score = min(score, 10)
    current_category = category

    result_label.config(
        text=f"Keywords: {', '.join(keywords)}\n"
             f"Score: {current_score}/10\n"
             f"Category: {category}"
    )


# 🔹 Upload PDF
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    if file_path:
        text = read_pdf(file_path)
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, text)


# 🔹 Export PDF Report
def export_pdf():
    if not current_keywords:
        messagebox.showwarning("Warning", "Analyze resume first!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF File", "*.pdf")])

    if file_path:
        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph("Resume Analysis Report", styles['Title']))
        content.append(Paragraph("<br/>", styles['Normal']))

        content.append(Paragraph(f"Keywords: {', '.join(current_keywords)}", styles['Normal']))
        content.append(Paragraph(f"Score: {current_score}/10", styles['Normal']))
        content.append(Paragraph(f"Category: {current_category}", styles['Normal']))

        doc.build(content)

        messagebox.showinfo("Success", "PDF Report saved successfully!")


# 🔹 GUI Setup
root = tk.Tk()
root.title("Resume Parser AI")
root.geometry("700x550")

# Title
tk.Label(root, text="Resume Parser", font=("Arial", 16, "bold")).pack(pady=10)

# Input box
input_text = tk.Text(root, height=12, width=80)
input_text.pack(pady=10)

# Buttons
tk.Button(root, text="Analyze", command=analyze_resume).pack(pady=5)
tk.Button(root, text="Upload PDF", command=upload_pdf).pack(pady=5)
tk.Button(root, text="Export Report (PDF)", command=export_pdf).pack(pady=5)

# Output
result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

# Run app
root.mainloop()
