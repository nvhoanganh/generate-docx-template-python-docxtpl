import base64
import copy
import json
import os
import shutil
import tempfile
import threading
import time
from io import BytesIO, open

import requests
from docxtpl import DocxTemplate, InlineImage, RichText
from flask import escape, jsonify, make_response, send_file
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Attachment, ContentId, Disposition,
                                   FileContent, FileName, FileType, Mail)

from airtable import getSpecReviewData, replaceBase64ImageFromUrl

sample = {
    "slug": "submit/201057845984868/",
    "q17_companyName": "Northwind Trader",
    "q36_yourName": {"first": "Anthony", "last": "Nguyen"},
    "q38_yourTitle": "Solution Architect",
    "q37_sendToEmailAddress": "anthonynguyen@ssw.com.au",
    "q27_projectName": "TraderOne v2",
    "q19_mainContact19": {
            "field_3": "John Smith",
            "field_4": "CTO",
        "field_5": "John@company.com",
        "field_6": "0412 345 675"
    },
    "q35_projectStakeholders_parse": [
        {
            "Name": "as",
            "Company": "dfasdfa",
            "Role": "Dev",
            "Email": "asdfa",
            "Mobile": "sdfasdf"
        }
    ],
    "file": "",
    "q39_majorFeatures_parse": [
            {"Name": "asdfa", "Description": "sdfasdfasdf"}
    ],
    "q40_outOfScope_parse": [{"Name": "asdfa", "Reason": "sdfasdf"}],
    "q42_assumptions_parse": [{"Name": "asdf", "Description": "asdfasdf"}],
    "q34_listOfPbi_parse": [
        {"PBI": "asdfasdfasdf", "Estimated_Hours": "1", "Is_MVP": "No"}
    ],
    "q41_totalEstimate": {
        "field_1": "86",
        "field_3": "54000",
        "field_4": "52500"
    },
    "q26_allRequirements": "NO",
    "q8_additionalComments": "asdfasdfasdf",
    "event_id": "1587172783013_201057845984868_zQc6pyA",
    "temp_upload": {
        "q31_img_highLevel": [
                "capture.png",
                "2020-04-17 22_38_10-main.py - generate_docx_from_template - Visual Studio Code.png"
        ]
    },
    "file_server": "go-sub-p0kw",
    "img_highLevel": [
        "https://www.jotform.com/uploads/nvhoanganh1909/201057845984868/4629822025226053817/2020-04-17%2022_38_10-main.py%20-%20generate_docx_from_template%20-%20Visual%20Studio%20Code.png",
        "https://www.jotform.com/uploads/nvhoanganh1909/201057845984868/4629822025226053817/capture.png"
    ]
}

# Set decode_content value to True, otherwise the downloaded image file's size will be zero.

# Copy the response stream raw data to local image file.
doc = DocxTemplate("jotformtemplate.docx")
doc.render(sample)
doc.save("output.docx")
