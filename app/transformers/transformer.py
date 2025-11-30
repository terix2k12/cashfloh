from pypdf import PdfReader


class Transformer:
    def pdf2text(self, pdf_path) -> str:
        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        return text
