from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

""" Обработчик POST-запросов формата http -f POST http://localhost:8080/albums artist="New Artist" genre="Rock" album="Super" и GET-запросов по адресу /albums/<artist>"""

# Обаботка GET запроса, выводит количество и список альбомов группы 
@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        albums_sum = len(albums_list)
        album_names = [album.album for album in albums_list]
        result = "Количество альбомов у {} - {}<br>".format(artist, albums_sum)
        result += "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def new_album():
    # проверяем, является ли введенный год числом
    test_year = album.is_number(request.forms.get("year"))
    if test_year is not False:
        album_data = {
            "year": int(test_year),
            "artist": request.forms.get("artist"),
            "genre": request.forms.get("genre"),
            "album": request.forms.get("album")
        }
        # проверяем, есть ли такой альбом в базе
        if album.find_album(album_data["artist"], album_data["album"]):
            message = "Альбом {} {} найден в базе".format(album_data["artist"], album_data["album"])
            result = HTTPError(409, message)
        else:
            if 0 <= album_data["year"] >= 2100:
                message = "Введены неверные данные поле год допускает значение от 0 до 2100"
                result = HTTPError(409, message)
            elif album_data["artist"].replace(" ", "") == "" or album_data["genre"].replace(" ", "") == "" or album_data["album"].replace(" ", "") == "":
                message = "Введены неверные данные поля артист, жанр или альбом не могут быть пустыми"
                result = HTTPError(409, message)
            else:
                album.album_add(album_data["year"], album_data["artist"], album_data["genre"], album_data["album"])
                result = "Альбом {} {} добавлен в базу".format(album_data["artist"], album_data["album"])
    else:
        message = "Введены неверные данные поле год содержит не числовые значения"
        result = HTTPError(409, message)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
