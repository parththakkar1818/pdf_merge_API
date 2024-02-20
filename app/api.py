from typing import Union, List

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfMerger
import os
from fastapi.responses import FileResponse, StreamingResponse

from io import BytesIO



app = FastAPI()

# Allow all origins for simplicity. In production, you should specify the allowed origins explicitly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with the list of allowed origins if you know them
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/sum") 
def add_two_numbers(number1: float, number2: float):
    """Add two numbers together"""
    result = number1+number2
    return {"result": result}


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@app.post('/merge')
async def merge(files: List[UploadFile] = File(...)):
    # Merge PDF files in memory
    merger = PdfMerger()
    for pdf in files:
        pdf_bytes = await pdf.read()
        merger.append(BytesIO(pdf_bytes))

    merged_pdf_bytes = BytesIO()
    merger.write(merged_pdf_bytes)
    merged_pdf_bytes.seek(0)

    return StreamingResponse(merged_pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=merged.pdf"})

# async def merge(pdfs: List[UploadFile] = File(...)):
#     create_upload_folder()

#     merger = PdfMerger()
#     filenames = []

#     for pdf in pdfs:
#         if pdf and allowed_file(pdf.filename):
#             filename = os.path.join(UPLOAD_FOLDER, pdf.filename)
#             with open(filename, 'wb') as f:
#                 f.write(pdf.file.read())
#             filenames.append(pdf.filename)
#             merger.append(filename)

#     output_filename = 'merged.pdf'
#     output_filepath = os.path.join(UPLOAD_FOLDER, output_filename)

#     with open(output_filepath, 'wb') as output_file:
#         merger.write(output_file)

#     return FileResponse(output_filepath, filename=output_filename)
