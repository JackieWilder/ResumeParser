import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json


def get_data(url=''):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    response = requests.get(url=url, headers=headers)

    
    soup = BeautifulSoup(response.text, 'lxml')

    card_links = [link['href'] for link in soup.find_all('a', class_='serp-item__title')]
    
    data = []


    for link in card_links:

        url = 'https://hh.ru' + link


        response = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        resume_title = soup.find('h2', class_='bloko-header-2').text
        
        work_experience = soup.find('h2', class_='bloko-header-2 bloko-header-2_lite').find('span', class_='resume-block__title-text resume-block__title-text_sub').text
        work_experience = ' '.join(work_experience.split()[2:])
        
        description = {}
        description['пол'] = soup.find('span', attrs={'data-qa': 'resume-personal-gender'}).text
        description['возраст'] = soup.find('span', attrs={'data-qa': 'resume-personal-age'}).text
        status = soup.find('div', class_='bloko-translate-guard').find('p').text.split(',')
        status = [i.strip() for i in status if not i.strip()[:2] == 'м.'][1:]
        description['статус'] = ' '.join(status)
    
        
        description['город'] = soup.find('span', attrs={'data-qa': 'resume-personal-address'}).text

        

  
        stackflow = []
        for div in soup.find_all('div', class_='bloko-tag-list'):
            spans = div.find_all('span')
            for span in spans:
                stackflow.append(span.text)


        resume = {
            'специальность': resume_title,
            'опыт работы': work_experience,
            'Ключевые навыки': stackflow,
            'описание': description,
            'ссылка на резюме': url
        }

        data.append(resume)
        print('added resume!')

    
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        

def main():
    proffesion = 'python' # further create the gui interface
    url = f'https://hh.ru/search/resume?text={proffesion}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false'
    
    get_data(url=url)


if __name__ == '__main__':
    main()



