from io import BytesIO
from docx import Document
from backend.services.file_parser import extract_text


def test_docx_parser():
    d = Document()
    d.add_paragraph("John Doe john@example.com Python SQL Bachelor")
    buf = BytesIO()
    d.save(buf)
    assert "Python" in extract_text(buf.getvalue(), ".docx")
