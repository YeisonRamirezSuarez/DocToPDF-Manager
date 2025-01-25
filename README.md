# 🌟 DocToPDF-Manager 🌟

## 📋 Description:
**DocToPDF-Manager** is a simple yet powerful tool designed to automate the conversion of Word documents (.docx) to high-quality PDF files, split PDFs into individual pages, and organize the results automatically. With its intuitive graphical interface built using Python and Tkinter, this application makes the entire PDF generation and management process efficient and user-friendly. 

## 🚀 Key Features:
- **📄 Word to PDF Conversion:** Effortlessly converts Word documents into high-quality PDFs.
- **🔄 Automatic Page Splitting:** Divides the generated PDFs into individual pages, making it easy to work with large documents.
- **📝 Smart Renaming:** Pages are automatically renamed based on information extracted from the content, like "Registration No." and the user’s name.
- **📂 Organized Management:** All the generated and split PDFs are saved in a neatly organized folder named after the original document.
- **👌 User-friendly Interface:** A simple, intuitive interface that requires no technical expertise to use.
- **⚡ Space Efficiency:** Once the PDF is processed, the original file is automatically deleted to free up space.

## 🧰 Technologies Used:
- **🐍 Python** - The main programming language used.
- **🖥 Tkinter** - For the graphical interface.
- **📑 PyPDF2 & PyMuPDF** - For handling PDF files (splitting, renaming, etc.).
- **📝 comtypes** - Used for automating Microsoft Word to convert DOCX files to PDF.

This tool is perfect for automating document management tasks, making it ideal for offices, educational institutions, and anyone who regularly handles Word and PDF files.

---

## ⚙️ How to Get Started:

### 1. Clone the repository:
```bash
git clone https://github.com/YourUsername/DocToPDF-Manager.git
cd DocToPDF-Manager
```

### 2. Install the necessary dependencies:
Make sure you have Python installed on your machine. Then, install the required libraries by running:
```bash
pip install tkinter PyPDF2 PyMuPDF comtypes
```

### 3. Run the application:
Once the dependencies are installed, simply run the following command to launch the application:
```bash
python generatePDFs.py
```
