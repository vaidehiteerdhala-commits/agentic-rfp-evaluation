from pathlib import Path
import pytest
from services.pdf_service import extract_pdf_text
def test_all_sample_pdfs_are_extractable():
 files=list(Path("data/sample_rfps").glob("*.pdf"));assert len(files)==4
 for f in files:
  text,pages=extract_pdf_text(f,True);assert pages>=2;assert len(text)>500
def test_invalid_pdf_rejected(tmp_path):
 p=tmp_path/"bad.pdf";p.write_bytes(b"bad")
 with pytest.raises(ValueError):extract_pdf_text(p)
