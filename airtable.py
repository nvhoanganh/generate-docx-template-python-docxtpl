from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from urllib.request import urlopen, urlretrieve
from docxtpl import DocxTemplate, InlineImage
import requests
import json
import time
import functools
import tempfile

baseUrl = 'https://api.airtable.com/v0/appkTAo6Zdydnm71L'
apiKey = 'keys78IGXc0nsZtoK'


def getRelated(resource, ids, selector):
    filter = ','.join(map(lambda id: 'RECORD_ID() = "{}"'.format(id), ids))
    data = requests.get('{}/{}?filterByFormula=OR({})'.format(baseUrl, resource, filter),
                        headers={'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(apiKey)})
    return list(map(selector, data.json()['records']))


def getSpecReviewData(projectId):
    # projectId = 'rec64QOSlzJ6QJEPO'
    resp = requests.get('{}/Projects/{}'.format(baseUrl, projectId), headers={
                        'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(apiKey)})

    project = resp.json()['fields']

    # airtable doesn't support loading related entities details, need to load manually
    pbis = [] if 'PBIs' not in project else getRelated('PBIs', project['PBIs'], lambda x: ({
        'name': x['fields']['Name'],
        'est': x['fields']['Estimated Hours'],
        'mvp': 'Y' if 'Is MVP?' in x['fields'] and x['fields']['Is MVP?'] else '',
        'bg': '42f557' if 'Is MVP?' in x['fields'] and x['fields']['Is MVP?'] else '',
        'std': '${:0,.0f}'.format(x['fields']['Estimated Hours'] * project['Avg Rate']),
        'pre': '${:0,.0f}'.format(x['fields']['Estimated Hours'] * project['Avg Rate (Discounted)'])
    }))

    features = [] if 'Project_Features' not in project else getRelated(
        'Project_Features', project['Project_Features'], lambda x: x['fields']['Name'])

    outScope = [] if 'Out of Scopes' not in project else getRelated(
        'Project_OutOfScopes', project['Out of Scopes'], lambda x: x['fields']['Name'])

    # airtable rate limit at 5 per second
    time.sleep(1)

    sswStaffs = [] if 'SSW Representatives' not in project else getRelated(
        'SSW_Staff', project['SSW Representatives'], lambda x: ({
            'name': x['fields']['Name'],
            'company': 'SSW',
            'role': x['fields']['Role'],
            'contact': {
                'mobile': x['fields']['Mobile'],
                'email': x['fields']['Email'],
            }
        }))

    productOwner = [] if 'Product Owner' not in project else getRelated(
        'Product_Owners', project['Product Owner'], lambda x: ({
            'name': x['fields']['Name'],
            'company': project['Customer Name'],
            'role': x['fields']['Title'],
            'contact': {
                'mobile': x['fields']['Mobile'],
                'email': x['fields']['Email'],
            }
        }))

    # final
    totalHours = 0 if 'PBIs' not in project else functools.reduce(
        lambda x, y: x + y, map(lambda t: t['est'], pbis))

    return {
        'author': {} if len(sswStaffs) == 0 else {
            'title': sswStaffs[0]['role'],
            'name': sswStaffs[0]['name']
        },
        'customer': {} if len(productOwner) == 0 else {
            'title': productOwner[0]['role'],
            'name': productOwner[0]['name']
        },
        'project': {
            'name': project['Project Name']
        },
        'title': '{} {} Specification Review'.format(project['Customer Name'], project['Project Name']),
        'parties': productOwner + sswStaffs,
        'ui_areas': features,
        'has_more': True,
        'outscope': outScope,
        'total': '{} h'.format(totalHours),
        'img_design': '' if 'High Level Design' not in project else project['High Level Design'][0]['url'],
        'std': '${:0,.0f}'.format(totalHours * project['Avg Rate']),
        'pre': '${:0,.0f}'.format(totalHours * project['Avg Rate (Discounted)']),
        'tasks': pbis
    }, project['Project Name']


def replaceBase64ImageFromUrl(doc, context):
    def toInlineImg(key):
        tmp_img_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')
        fsrc = urlopen(context[key])

        print('Downloading {} to {}'.format(context[key], tmp_img_file.name))
        copyfileobj(fsrc, tmp_img_file)
        # dst = 'downloaded.jpg'
        # urlretrieve(context[key], dst)
        context[key] = InlineImage(doc, tmp_img_file.name)
        return tmp_img_file.name

    return [toInlineImg(k) for k in context.keys() if k.startswith('img_') and context[k] != '']


if __name__ == '__main__':
    # local test
    doc = DocxTemplate("template.docx")
    data, name = getSpecReviewData('rec64QOSlzJ6QJEPO')
    tempFiles = replaceBase64ImageFromUrl(doc, data)
    doc.render(data)
    doc.save("output.docx")
