import requests
from bs4 import BeautifulSoup
import json


def get_all_movie_Data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    infobox = soup.find(class_="infobox vevent")
    info_rows = infobox.find_all("tr")
    movie_info = {}

    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info["title"] = row.find("th").get_text()
        elif index == 1:
            continue
        else:
            content_key = row.find("th").get_text(" ", strip=True)
            content_value = get_content_data(row.find("td"))
            movie_info[content_key] = content_value

    return movie_info


def get_content_data(rows_data):
    if rows_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ") for li in rows_data.find_all("li")]
    else:
        return rows_data.get_text(" ", strip=True).replace("\xa0", " ")


def get_all_movie_links():
    r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
    soup = BeautifulSoup(r.content, "html.parser")

    movies = soup.select(".wikitable.sortable i a")

    base_path = "https://en.wikipedia.org/"

    movie_data_list = []

    for index, movie in enumerate(movies):
        try:
            relatif_path = movie["href"]
            full_path = base_path + relatif_path
            title = movie["title"]
            movie_data_list.append(get_all_movie_Data(full_path))

        except Exception as e:
            print(movie.get_text())
            print(e)
            
    return movie_data_list

def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(title):
    with open(title, encoding='utf-8') as f:
        return json.load(f)
def save_movies_data():
    data = get_all_movie_links()
    save_data("disney_movies_data", data)
    
save_movies_data()