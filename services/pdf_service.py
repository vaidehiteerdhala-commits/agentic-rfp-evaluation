import fitz
def extract_pdf_text(source,include_metadata=False):
 raw=source.getvalue() if hasattr(source,"getvalue") else open(source,"rb").read()
 if not raw or len(raw)<20:raise ValueError("The uploaded PDF is empty or invalid.")
 try:doc=fitz.open(stream=raw,filetype="pdf")
 except Exception as exc:raise ValueError(f"The file could not be opened as a PDF: {exc}") from exc
 if doc.page_count==0:raise ValueError("The PDF contains no pages.")
 blocks=[]
 for n,page in enumerate(doc,1):
  text=page.get_text("text").strip()
  if text:blocks.append(f"[PAGE {n}]\n{text}")
 combined="\n\n".join(blocks).strip()
 if len(combined)<80:raise ValueError("No reliable extractable text was found. The PDF may require OCR.")
 return (combined,doc.page_count) if include_metadata else combined
