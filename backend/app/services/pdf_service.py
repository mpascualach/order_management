import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

class PDFService:
  @staticmethod
  def generate_order_pdf(order):
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template('order_template.html')

    html_content = template.render(order=order)

    pdf_directory = 'app/static/pdfs'
    os.makedirs(pdf_directory, exist_ok=True)
    pdf_path = os.path.join(pdf_directory, f'order_{order.id}.pdf')

    pdfkit.from_string(html_content, pdf_path)

    return pdf_path