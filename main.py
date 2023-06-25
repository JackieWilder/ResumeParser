import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json


def get_data(url=''):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    # чтобы заработало нужно раскомментить
    response = requests.get(url=url, headers=headers)

    
    soup = BeautifulSoup(response.text, 'lxml')
    #получаем ссылки на все резюме на странице
    card_links = [link['href'] for link in soup.find_all('a', class_='serp-item__title')]
    
    data = []

    # парсим карточку
    for link in card_links:
        # делаем запрос на ссылку карточки
        url = 'https://hh.ru' + link
        # print(url)

        response = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        # ищем интересующие нас параметры
        resume_title = soup.find('h2', class_='bloko-header-2').text
        # print(resume_title)
        work_experience = soup.find('h2', class_='bloko-header-2 bloko-header-2_lite').find('span', class_='resume-block__title-text resume-block__title-text_sub').text
        work_experience = ' '.join(work_experience.split()[2:])
        # print(work_experience)
        description = {}
        description['Gender'] = soup.find('span', attrs={'data-qa': 'resume-personal-gender'}).text
        description['Age'] = soup.find('span', attrs={'data-qa': 'resume-personal-age'}).text
        status = soup.find('div', class_='bloko-translate-guard').find('p').text.split(',')
        status = [i.strip() for i in status if not i.strip()[:2] == 'м.'][1:]
        description['Status'] = ' '.join(status)
    
        
        description['City'] = soup.find('span', attrs={'data-qa': 'resume-personal-address'}).text

        # print(description)

  
        stackflow = []
        for div in soup.find_all('div', class_='bloko-tag-list'):
            spans = div.find_all('span')
            for span in spans:
                stackflow.append(span.text)
        # print(stackflow)

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
    proffesion = 'Слесарь' # в дальнейшем включить в интерфейс взаимодействия с пользователем 
    url = f'https://hh.ru/search/resume?text={proffesion}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false'
    
    get_data(url=url)


if __name__ == '__main__':
    main()



