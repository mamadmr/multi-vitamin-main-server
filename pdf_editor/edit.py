import fitz
import arabic_reshaper
from bidi.algorithm import get_display
import unicodedata

myfont = "/Users/trx/Documents/Projects/multi-vitamin-main-server/Fonts/‌‌badr.ttf"
font_size = 15
font_color = (0, 0, 0)

def add(point, text, page):
    '''
        point: tuple of (x, y)
        text: string
        page: page of pdf
    '''
    # check if the text is in persian
    name = unicodedata.name(text[0]).lower()

    if 'arabic' in name or 'persian' in name:
        # insert font
        page.insert_font(fontname="F0", fontfile=myfont)
        text = arabic_reshaper.reshape(text)    # correct its shape
        text = get_display(text)           # correct its direction
        page.insert_text(point, 
                     text,  
                     fontsize = font_size,  
                     color = font_color,  # some color: black
                     fontname='F0'
                )
    else:
        page.insert_text(point,
                     text, 
                     fontsize = font_size, 
                     color = font_color, 
                )

def first_page(page, info):
    # fill the headers of the page
    data = info['headers']['question_number']
    add((325 , 112), data, page)

    data = info['headers']['subject']
    add((325 , 133), data, page)

    data = info['headers']['hardness']
    add((325 , 155), data, page)

    data = info['headers']['date']
    add((170 , 112), data, page)

    data = info['headers']['price']
    add((170 , 134), data, page)

    data = info['headers']['team_number']
    add((70 , 112), data, page)

    data = info['headers']['team_name']
    add((70 , 132), data, page)

    data = info['headers']['score']
    add((70 , 158 ), data, page)
    # fill the questions and scores
    for i in range(len(info['questions'])):
        data = info['questions'][i][0]
        add((530 , 220 + i * 26.2), data, page)
        data = info['questions'][i][1]
        add((470 , 220 + i * 26.2), data, page)
    
    # fill the subjects and total scores
    for i in range(len(info['subjects'])):
        data = info['subjects'][i][0]
        add((325 , 638 + i * 18.8), data, page)
        data = info['subjects'][i][1]
        add((265 , 638 + i * 18.8), data, page)
        data = info['subjects'][i][2]
        add((195 , 638 + i * 18.8), data, page)
        

def second_page(page, info):
    data = info['headers']['team_number']
    add((300, 85), data, page)
    data = info['headers']['question_number']
    add((420, 85), data, page)

def edit(location, info):
    '''
    location: pdf file location
    info: dict of info (headrs, list of questions and scores, list of subjects and total scores)
    '''
    doc = fitz.open(location)  # new or existing PDF
    page_count = doc.page_count
    first_page(doc[0], info)
    if(page_count == 2):
        second_page(doc[1], info)
    doc.save("to_send_files/"+info['headers']['team_number']+'_'+info['headers']['question_number']+".pdf") 

if __name__ == '__main__':
    location = "/Users/trx/Documents/Projects/multi-vitamin-main-server/Template_pdf/print21.pdf"
    doc = fitz.open(location)  # new or existing PDF
    page = doc[0] # new or existing page via doc[n]
    info = {
            "headers": {
              'team_name': 'تیم ۱',
              'team_number':'15', 
              'date':'12:00', 
              'price':'200', 
              'question_number':'1234', 
              'subject':'ریاضی',
              'hardness':'سخت',
              'score': '20'
              },
            "questions": [ 
                ['A234','50'],
                ['A235', '20'],
                ['A236', '40'],
                ['A234','50'],
                ['A235', '20'],
                ['A236', '40'],
                ['A234','50'],
                ['A235', '20'],
                ['A236', '40'],
                ['A234','50'],
                ['A235', '20'],
                ['A236', '40'],
                ['A234','50'],
                ['A235', '20'],
                ['A236', '40'],
                ['A236', '40'],
                ['A234','50'],
                ['A235', '20'],
                ['A236', '40'],
                ['A234','50'],
                ['A235', '20'],
                ['A236', '40'],
                ['A236', '40'],
                ],
            "subjects": [
                ['math', '500', '2'],
                ['science', '300', '1'],
                ['english', '200', '1'],
                ['math', '500', '2', '5'],
                ['science', '300', '1'],
                ['english', '200', '1'],
                ['math', '500', '2',],
                ['science', '300', '1'],
                ['english', '200', '1'],
                ]
            }
    edit(location, info)
