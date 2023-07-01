from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    # отправляем GET-запрос и получаем HTML-страницу
    html_page = requests.get("https://halleylabs.com/album/d-freq-crush").content

    # инициализируем объект BeautifulSoup и передаем ему HTML-страницу
    soup = BeautifulSoup(html_page, 'html.parser')

    # находим ссылку на обложку альбома
    href_profile = [a.get('href') for a in soup.find_all('a', class_='pic')]

    # находим все теги <img> с классом "thumb"
    img_profile = [img.get('src').replace('_42.jpg', '_23.jpg') for img in soup.find_all('img', class_='thumb')]

    # находим все div-элементы с классом name
    name_profile = [div.text for div in soup.find_all('div', {'class': 'name'})]

    # формируем список кортежей из данных об альбомах
    albums = []
    for i in range(len(name_profile)):
        album = {
            'name': name_profile[i],
            'href': href_profile[i],
            'img': img_profile[i]
        }
        albums.append(album)

    # возвращаем шаблон с данными об альбомах
    return render_template('index.html', albums=albums)

if __name__ == '__main__':
    app.run(debug=True)