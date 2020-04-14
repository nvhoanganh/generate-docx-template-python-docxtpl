from docxtpl import DocxTemplate, RichText, InlineImage
from flask import escape, send_file, make_response, jsonify
from io import open, BytesIO
from airtable import getSpecReviewData
import tempfile
import base64
import os
import json


def json2docx(request):
    doc = DocxTemplate("template.docx")
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_args and 'data' in request_args:
        request_json = json.loads(request_args['data'])

    # replace base64 image with temp file
    tempFiles = replaceBase64Image(doc, request_json)

    doc.render(request_json)
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    # Delete tmp file
    [os.unlink(f) for f in tempFiles]
    response = send_file(file_stream, as_attachment=True,
                         attachment_filename=request_json['title'] + '.docx')

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    return response


def airtable2docx(request):
    doc = DocxTemplate("template.docx")
    data, projectName = getSpecReviewData(request.args['projectId'])
    doc.render(data)
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    response = send_file(file_stream, as_attachment=True,
                         attachment_filename=projectName + '.docx')

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    return response


def template(request):
    file_stream = open("template.docx", "rb")
    return send_file(file_stream, as_attachment=True,
                     attachment_filename='template.docx')


def version(request):
    response = make_response(
        jsonify({"version": "0.1.0"}), 200)

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response


def replaceBase64Image(doc, context):
    def toInlineImg(key):
        tmp_img_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')
        tmp_img_file.write(base64.urlsafe_b64decode(context[key]))
        tmp_img_file.close()

        context[key] = InlineImage(doc, tmp_img_file.name)
        return tmp_img_file.name

    return [toInlineImg(k) for k in context.keys() if k.startswith('img_')]
