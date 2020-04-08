from docxtpl import DocxTemplate, RichText, InlineImage

doc = DocxTemplate("templates/template.docx")


def renderContact(doc, mobile, email):
    rt = RichText('')
    rt.add(email, url_id=doc.build_url_id(
        'mailto:{}'.format(email)), underline=True, color='#3495eb')
    rt.add('\n{}'.format(mobile))
    return rt


context = {
    'author': {
        'title': 'Solution Architect',
        'name': 'Anthony Nguyen',
    },
    'customer': {
        'title': 'Product Owner',
        'name': 'John Charles',
    },
    'project': {
        'name': 'SUPERCOOLA POS',
    },
    'title': "SUPERCOOLA POS Specification Review",
    'parties': [
        {
            'name': 'John Charles',
            'company': 'SUPERCOOLA',
            'role': 'Product Owner',
            'contact': renderContact(doc, '+61 433 333 222', 'John@SUPERCOOLA.com')
        },
        {
            'name': 'Anthony Nguyen',
            'company': 'SSW',
            'role': 'Project Manager',
            'contact': renderContact(doc, '+61 433 219 388', 'anthony@ssw.com.au')
        },
        {
            'name': 'Michael Smedley',
            'company': 'SSW',
            'role': 'Scrum Master',
            'contact': renderContact(doc, '+61 433 111 000', 'michael@ssw.com.au')
        },
    ],
    'design': InlineImage(doc, 'design.png'),
    'ui_areas': [
        'Login and Sign up page',
        'Home page',
        'Report',
        'Checkout'
    ],
    'has_more': True,
    'outscope': [
        'Payment gateway',
        'Support after deployment'
    ],
    'total': '230 h',
    'std': '$33,400',
    'pre': '$30,400',
    'tasks': [
        {
            'name': 'Login screen',
            'est': '16 h',
            'std': '$4,100',
            'pre': '$3,800',
            'bg': '42f557',
            'mvp': 'Y'
        },
        {
            'name': 'Sign up screen',
            'est': '8 h',
            'std': '$2,100',
            'pre': '$1,800',
            'bg': '42f557',
            'mvp': 'Y'
        },
        {
            'name': 'Google Sign In',
            'est': '16 h',
            'std': '$4,100',
            'pre': '$3,800',
        },
    ]

}
doc.render(context)
doc.save("output/output.docx")
