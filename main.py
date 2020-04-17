from docxtpl import DocxTemplate, RichText, InlineImage
from flask import escape, send_file, make_response, jsonify
from io import open, BytesIO
from airtable import getSpecReviewData, replaceBase64ImageFromUrl
import tempfile
import requests
import copy
import base64
import time
import os
import shutil
import json
import threading
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient


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
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    return response


def multipart(request):
    data = request.form.to_dict()
    jdata = {'processed': True}

    if 'rawRequest' in data:
        args = request.args
        jdata = json.loads(data['rawRequest'])

        def parseJsonKey(k):
            jdata[k] = json.loads(jdata[k])

        def getProperty(property):
            return jdata[next((k for k in jdata.keys() if k.endswith(property)), None)]

        # Replace the key that are in Raw JSON format by parsing it
        [parseJsonKey(k) for k in jdata.keys() if k.endswith('_parse')]

        print(json.dumps(jdata))
        filename = '{}{}'.format(
            getProperty(args['filename']), args['suffix'])
        # Send email
        print('Starting work on new Thread')
        thread1 = threading.Thread(
            target=prepareAndSend,
            args=(getProperty(args['email']),
                  filename,
                  '{}.docx'.format(filename),
                  jdata,
                  os.environ.get('SENDGRID_API_KEY')))
        thread1.start()

    return jsonify(jdata)


def prepareAndSend(to, subject, filename, jdata, sendGridApi):
    sendEmail(to=to,
              subject=subject,
              filename=filename,
              content=mergeDoc(
                  'jotformtemplate.docx', jdata).read(),
              apikey=sendGridApi)


def airtable2docx(request):
    doc = DocxTemplate("template.docx")
    data, projectName = getSpecReviewData(request.args['projectId'])

    # replace image from URL
    tempFiles = replaceBase64ImageFromUrl(doc, data)

    doc.render(data)
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    # Delete tmp file
    [os.unlink(f) for f in tempFiles]

    response = send_file(file_stream, as_attachment=True,
                         attachment_filename=projectName + '.docx')

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    return response


def template(request):
    response = file_stream = open("jotformtemplate.docx", "rb")
    response.headers['Cache-Control'] = 'no-cache'
    return response


def replaceBase64Image(doc, context):
    def toInlineImg(key):
        tmp_img_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')
        tmp_img_file.write(base64.urlsafe_b64decode(context[key]))
        tmp_img_file.close()

        context[key] = InlineImage(doc, tmp_img_file.name)
        return tmp_img_file.name

    return [toInlineImg(k) for k in context.keys() if k.startswith('img_')]


def sendEmail(to, subject, filename, content, apikey):
    # Attachment
    print('Sending the doc to {}'.format(to))
    message = Mail(
        from_email='noreply@json2docx.com',
        to_emails=to,
        subject=subject,
        html_content='<p>Attached: {}</p>'.format(filename))

    encoded = base64.b64encode(content).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType(
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition('attachment')

    message.attachment = attachment
    # sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    print('sending the email now using api key {}'.format(apikey))
    sendgrid_client = SendGridAPIClient(apikey)
    response = sendgrid_client.send(message)
    print('Email sent with response code {}'.format(response.status_code))


def mergeDoc(template, request_json):
    doc = DocxTemplate(template)
    tempFiles = []
    try:
        # replace base64 image with temp file
        newJson = copy.deepcopy(request_json)
        tempFiles = replaceBase64ImageFromUrl(doc, newJson)

        doc.render(newJson)
    except Exception as e:
        print('Error generating document,error is {}'.format(e))
        doc.render(request_json)
    finally:
        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        [os.unlink(f) for f in tempFiles if f != '']
        return file_stream
