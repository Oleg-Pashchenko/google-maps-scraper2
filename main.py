from src import Gmaps
import dataclasses
import re
import requests
import pandas as pd


def find_emails_and_phones(url):
    if url is None:
        return None, None
    if not 'http' in url:
        url = 'https://' + url
    try:
        response = requests.get(url)
    except:
        return None, None
    if response.status_code == 200:
        # Используем регулярные выражения для поиска электронных адресов
        emails = re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', response.text)
        # Используем регулярные выражения для поиска телефонных номеров
        phones = re.findall(r'\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b', response.text)
        return set(emails), set(phones)
    else:
        print("Ошибка при получении страницы:", response.status_code)
        return None, None


@dataclasses.dataclass
class WebSite:
    name: str
    link: str
    address: str
    website: str
    phone: str
    email: str

    def __str__(self):
        return f'<a href="{self.link}">Ссылка</a>\n{self.address}\nСайт: {self.website}\nНомера: {self.phone}\nПочты: {self.email}'


def search(query: str):
    websites = set()
    answers = []
    results = Gmaps.places([query])
    for result in results['places']:
        website = result['website']
        if website in websites:
            continue
        websites.add(website)

        phone, email = find_emails_and_phones(website)
        answer = WebSite(
            result['name'],
            result['link'],
            result['address'],
            website,
            email,
            phone
        )
        answers.append(answer)
    return answers

def execute_query(query):
    answer = search(query=query)
    data_dict = [{field.name: getattr(person, field.name) for field in WebSite.__dataclass_fields__.values()} for person in
                 answer]
    df = pd.DataFrame(data_dict)
    df.to_excel(f"answer.xlsx", index=False)
