from docxtpl import DocxTemplate, RichText, InlineImage
from flask import escape, send_file
from io import open, BytesIO
import tempfile
import base64
import os


def json2docx(request):
    doc = DocxTemplate("template.docx")
    request_json = request.get_json(silent=True)

    # replace base64 image with temp file
    tempFiles = replaceBase64Image(doc, request_json)

    doc.render(request_json)
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    # Delete tmp file
    [os.unlink(f) for f in tempFiles]

    return send_file(file_stream, as_attachment=True, attachment_filename='output.docx')


def template(request):
    file_stream = open("template.docx", "rb")
    return send_file(file_stream, as_attachment=True, attachment_filename='template.docx')


def replaceBase64Image(doc, context):
    def toInlineImg(key):
        tmp_img_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')
        tmp_img_file.write(base64.urlsafe_b64decode(context[key]))
        tmp_img_file.close()

        context[key] = InlineImage(doc, tmp_img_file.name)
        return tmp_img_file.name

    return [toInlineImg(k) for k in context.keys() if k.startswith('img_')]
