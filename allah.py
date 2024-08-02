import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
import io
from openpyxl import Workbook

def extract_invoice_details(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text()

    # Extracting specific details from the text
    invoice_details = {
        "Invoice Number": extract_detail(text, "Numéro", "Date échéance"),
        "Invoice Date": extract_detail(text, "Date", "Numéro"),
        "Due Date": extract_detail(text, "Date échéance", "N° de Tva intracom"),
        "Client Code": extract_detail(text, "Code client", "Date"),
        "Payment Terms": extract_detail(text, "Mode de règlement", "Code client"),
        "Solde dû": extract_saldo_due(text)
    }

    return invoice_details

def extract_detail(text, start_keyword, end_keyword):
    start = text.find(start_keyword) + len(start_keyword)
    end = text.find(end_keyword, start)
    return text[start:end].strip().split("\n")[0].strip()

def extract_saldo_due(text):
    end_marker = "Escompte pour règlement anticipé"
    start = text.rfind("Solde dû")
    end = text.rfind(end_marker)
    if start != -1 and end != -1:
        # Extract the relevant part and clean up extra symbols
        saldo_due = text[start:end].strip().split("\n")[-1].strip()
        # Use regex to clean up extra Euro symbols
        saldo_due = re.sub(r'(€)\1+', r'\1', saldo_due)  # Replace multiple € with a single €
        return saldo_due
    return "Not found"

def create_excel_file(data):
    # Create an Excel workbook and add a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice Details"

    # Add headers
    headers = list(data.keys())
    ws.append(headers)

    # Add data row
    row = [data[key] for key in headers]
    ws.append(row)

    # Save the workbook to a binary stream
    excel_stream = io.BytesIO()
    wb.save(excel_stream)
    excel_stream.seek(0)
    
    return excel_stream

st.title("Invoice PDF Extractor")
uploaded_file = st.file_uploader("Upload your invoice PDF", type="pdf")

if uploaded_file is not None:
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    details = extract_invoice_details("uploaded_file.pdf")

    # Create a DataFrame with a single row and custom column names
    df = pd.DataFrame([details], columns=[
        "Invoice Number",
        "Invoice Date",
        "Due Date",
        "Client Code",
        "Payment Terms",
        "Solde dû"
    ])

    st.write("Invoice Details (Single Row):")
    
    # Convert DataFrame to HTML
    html = df.to_html(index=False, classes='dataframe', border=0)
    
    # Display HTML table
    st.markdown(
        f"""
        <div style="overflow-x: auto; white-space: nowrap;">
            {html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create and provide a download link for the Excel file
    excel_file = create_excel_file(details)
    st.download_button(
        label="Download as Excel",
        data=excel_file,
        file_name="invoice_details.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
