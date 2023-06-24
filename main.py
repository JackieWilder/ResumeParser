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
    #response = requests.get(url=url, headers=headers)
    #print(response.text)
    #with open('index.html', 'w') as file:
        #file.write(response.text)

    with open('index.html', 'r') as file:
        src = file.read()
    

    soup = BeautifulSoup(src, 'lxml')
    #получаем ссылки на все резюме на странице
    card_links = [link['href'] for link in soup.find_all('a', class_='serp-item__title')]
    
    data = []

    # парсим карточку
    for link in card_links[:1]:
        # делаем запрос на ссылку карточки
        url = 'https://hh.ru' + link
        # print(url)

        response = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        # ищем интересующие нас параметры
        resume_link = url
        resume_title = soup.find('h2', class_='bloko-header-2').text
        # print(resume_title)
        work_experience = soup.find('h2', class_='bloko-header-2 bloko-header-2_lite').text.replace('\xa0', ' ')
        # print(work_experience)
        description = {}
        text = [i for i in soup.find('div', id='a11y-main-content').find_all('p') if i.text]
        
        # МОЖЕТ ВЫСКОЧИТЬ ОШИБКА ЕСЛИ ТЕКСТА НЕ БУДЕТ
        p1, p2 = text
        p1, p2 = p1.text.split(','), p2.text.split(',')
        
        # АНАЛОГИЧНО
        description['пол'] = p1[0]
        description['возраст'] = p1[1].replace('\xa0', ' ').split()[0].strip()
        description['статус'] = str(p2[1].strip()) + ', ' + str(p2[2].strip())
        description['город'] = p2[0]

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

    
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        









def get_soup():
    pass


def main():
    proffesion = 'python' # в дальнейшем включить в интерфейс взаимодействия с пользователем 
    url = f'https://hh.ru/search/resume?text={proffesion}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false'
    
    get_data(url=url)


if __name__ == '__main__':
    main()



