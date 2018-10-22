import os
import json
from time import sleep
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import yagmail


def check_anns(anns, jl_path, sent=True):
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
        # Retrieve the title text of the announcement.
        title = ann.a.text

        # Data saved in .jl file contain unicode so it is necessary to convert
        # the title string into proper format to compare wheter
        # it is in the file.
        if json.dumps(title) not in text:
            # Create a dictionary to populate the file.
            d = dict()

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


def download_anns(site):
    """
    Scrape announcements from site.
    """
    r = requests.get(site, timeout=20)
    if r.ok:
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        anns = soup.find_all('div', {'class': 'class-blog-post'})

        return anns
    else:
        return "Bad response"


def send_mail(jl_path):
    # Open file containing scraped data.
    file = open(jl_path, 'a+')
    file.seek(0, 0)

    # Read content of the file.
    content = file.read().split('\n')

    for line in content:
        try:
            line = json.loads(line)
        except json.decoder.JSONDecodeError:
            # Except error on the last iteration,
            # because the file contain blank line at the end.
            break
        if line["sent"] is False:
            yag = yagmail.SMTP()
            contents = [line["content"]]
            yag.send('...', line["title"], contents)
            line["sent"] = True
            print('Mail sent.')


def main():
    while True:
        site = 'http://www.elka.pw.edu.pl/Aktualnosci/Komunikaty-Dziekanatu'
        anns = download_anns(site)

        jl_path = 'announcement.jl'
        if os.path.isfile(jl_path):
            # If .jl file exists append file with new announcements
            # and define them as not sent to the user.
            check_anns(anns=anns, jl_path='announcement.jl', sent=False)
        else:
            # If .jl file does not exist assume user
            # already read all the announcements
            # on the webpage and define them as sent.
            check_anns(anns=anns, jl_path='announcement.jl', sent=True)

        send_mail(jl_path)
        print(str(datetime.now()) + ': Waiting 6 hours')

        sleep(21600)


if __name__ == "__main__":
    main()
