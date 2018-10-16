import os
import json

import requests
from bs4 import BeautifulSoup

def check_anns(anns, jl_path='announcement.jl', sent=True):
    """
    Attempt to check wheter scraped data contain new announcement
    and append it to the .jl file.

    Args:
        anns (bs4.element.ResultSet): Scraped announcements from site.
        jl_path (str): Path to .jl file containing saved announcements.
        sent (bool): Wheter message was sent to the user.
    """
    # Open file containing scraped data.
    file = open(jl_path, 'a+')
    file.seek(0, 0)

    # Read content of the file.
    text = file.read()

    for ann in anns:
        # Create a dictionary to populate the file.
        d = dict()

        # Retrieve the title text of the announcement.
        title = ann.a.text

        # Data saved in .jl file contain unicode so it is necessary to convert
        # the title string into proper format to compare wheter
        # it is in the file.
        if json.dumps(title) not in text:

            # Populate the dictionary and save it into file.
            d['title'] = title
            d['content'] = ann.p.text
            d['sent'] = sent
            new_line = json.dumps(d) + "\n"
            file.write(new_line)
        else:
            # If announcement exist in the list, brake early from the for loop.
            break
    file.close()

def download_anns(site='http://www.elka.pw.edu.pl/Aktualnosci/Komunikaty-Dziekanatu'):
    """
    Scrape announcements from site.
    """
    r = requests.get(site)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    anns = soup.find_all('div', {'class': 'class-blog-post'})

    return anns



if __name__ == "__main__":

    anns = download_anns()

    jl_path='announcement.jl'
    if os.path.isfile(jl_path):
        # If .jl file exists append file with new announcements
        # and define them as not sent to the user.
        check_anns(anns=anns, jl_path='announcement.jl', sent=False)
    else:
        # If .jl file does not exist assume user already read all the announcements
        # on the webpage and define them as sent.
        check_anns(anns=anns, jl_path='announcement.jl', sent=True)
