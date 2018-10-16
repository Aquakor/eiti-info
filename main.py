import os
import json

import requests
from bs4 import BeautifulSoup

def check_anns(anns, jl_path='announcement.jl', sent=True):
    file = open(jl_path, 'a+')
    file.seek(0, 0)
    text = file.read()

    for ann in anns:
        d = dict()
        title = ann.a.text
        if json.dumps(title) not in text:
                d['title'] = title
                d['content'] = ann.p.text
                d['sent'] = sent
                new_line = json.dumps(d) + "\n"
                file.write(new_line)
        else:
            # If announcement exist in the list brake early from the for loop.
            break
    file.close()


if __name__ == "__main__":

    site = 'http://www.elka.pw.edu.pl/Aktualnosci/Komunikaty-Dziekanatu'
    r = requests.get(site)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    anns = soup.find_all('div', {'class': 'class-blog-post'})

    file_path = 'announcement.jl'
    if os.path.isfile(file_path):
        check_anns(anns=anns, jl_path=file_path, sent=False)
    else:
        check_anns(anns=anns, jl_path=file_path, sent=True)
