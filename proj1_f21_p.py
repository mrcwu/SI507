

class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        if (json != None):
            self.title = json['collectionName']
            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]
            self.url = json['collectionViewUrl']
        else:
            self.title = str(title)
            self.author = str(author)
            self.release_year = release_year
            self.url = str(url)


    def info(self):
        return self.title + " by " + self.author + " (" + str(self.release_year) + ")"

    def length(self):
        return 0


# Other classes, functions, etc. should go here
class Song(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
        # super().__init__(author, release_year)
        if (json != None):
            self.title = json['trackName']
            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]
            self.url = json['trackViewUrl']
            self.album = json['collectionName']
            self.genre = json['primaryGenreName']
            self.track_length = json['trackTimeMillis']
        else:
            self.title = str(title)
            self.author = str(author)
            self.release_year = release_year
            self.url = str(url)
            self.album = str(album)
            self.genre = str(genre)
            self.track_length = track_length


    def info(self):
        return super().info() + " [" + str(self.genre) +"]"

    def length(self):
        return round(self.track_length/1000,0)


class Movie(Song):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
        # Media.__init__(self, author, release_year)
        # Song.__init__(self, title, url)
        if (json != None):
            self.title = json['trackName']
            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]
            self.url = json['trackViewUrl']
            self.rating = json['contentAdvisoryRating']
            self.movie_length = json['trackTimeMillis']
        else:
            self.title = str(title)
            self.author = str(author)
            self.release_year = release_year
            self.url = str(url)
            self.rating = rating
            self.movie_length = movie_length


    def info(self):
        return Media.info(self) + " [" + str(self.rating) + "]"

    def length(self):
        return round(self.movie_length/60000,0)

# part 3
import requests as re
import json

url = "https://itunes.apple.com/search?term=america"
raw_data = re.get(url)
data = json.loads(raw_data.text)
result = data['results']


# part 4
if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here

    term = input('''Enter a search term, or "exit" to quit:''')
    while term != "exit":
        url = "https://itunes.apple.com/search?term=" + str(term)
        raw_data = re.get(url)
        data = json.loads(raw_data.text)
        result = data['results']

        if result != []:
            songs = []
            movies = []
            medias = []
            dict = {'Song': songs, 'Movie': movies, 'Media': medias}

            for i in result:
                if i['wrapperType'] == 'track':
                    if i['kind'] == 'song':
                        songs.append(Song(json=i))
                    elif i['kind'] == 'feature-movie':
                        movies.append(Movie(json=i))
                    else:
                        medias.append(Media(json=i))
                else:
                    medias.append(Media(json=i))

            count = 1
            for lst in dict:
                print(lst)
                for m in dict[lst]:
                    print(str(count) + " " + m.info())
                    count += 1
        total = songs + movies + medias
        term = input('Enter a number for more info, or another search term, or exit:')

        while True:
            try:
                print('Launching' + '\n' + total[int(term) - 1].url + '\n' + 'in web browser...')
                term = input('Enter a number for more info, or another search term, or exit:')
            except:
                break



    if term == 'exit':
        print('Bye!')
