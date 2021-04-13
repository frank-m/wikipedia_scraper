from bs4 import BeautifulSoup
import requests
import os
import json


class Collection:
    def __init__(self, name: str):
         self.name = name
    
    def get_item(self, _item_list: str, number: int):
        return next((item for item in _item_list if item.number == number), None)

    def add_item(self, classDef, _item_list: str, number: int, *args):
        if not self.get_item(_item_list, number):
            _item_list.append(classDef(number, *args))
        else:
            print(f"{classDef.name} {number} already exists in {self.name}")

    def write_out(self, location, _item_list, classDef=None):
        path = location + '/' + self.name
        if not os.path.isdir(path):
            os.mkdir(path)

        if classDef:
            for item in _item_list:
                classDef.write_out(item, path)
        else: 
            filename = path + '/' + self.name + '.json'
            with open(filename, 'w') as outfile:
                json.dump([item.__dict__ for item in _item_list], outfile)

class TVShow(Collection):
    def __init__(self, name: str, year: str):
        self.name = name
        self.year = year
        self._seasons = []

    @property
    def seasons(self):
        return self._seasons

    def get_season(self, season_number: int):
        return super().get_item(self._seasons, season_number)  


    def add_season(self, season_number: int):
        return super().add_item(Season, self._seasons, season_number, self.name)


    def get_episode(self, season_number: int, episode_number: int):
        season = self.get_season(season_number)
        if season:
            return season.get_episode(episode_number)
        else:
            print(f"The Season {season_number} does not exist.")
            

    def add_episode(self, season_number: int, episode_number: int, name: str, date: str):
        season = self.get_season(season_number)
        if season:
            season.add_episode(episode_number, name, date)
        else:
            print(f"The Season {season_number} does not exist.")

    def write_out(self, location):
        super().write_out(location, self._seasons, Season)


class Season(Collection):
    def __init__(self, number: int, show: str):
        self.name = f"Season {number}"
        self.number = number
        self.show = show
        self._episodes = []

    @property
    def episodes(self):
        return self._episodes

    def get_episode(self, episode_number):
        return super().get_item(self._episodes, episode_number) 

    def add_episode(self, episode_number: int, name: str, date: str):
        return super().add_item(Episode, self._episodes, episode_number, name, date, self.number, self.show)

    def write_out(self, location):
        super().write_out(location, self._episodes)


class Episode:
    def __init__(self, number: int, name: str, date: str, season: int, show: str):
        self.number = number
        self.name = name
        self.date = date
        self.season = season
        self.show = show



show = TVShow('Fringe', 2008)

show.add_season(1)

show.add_episode(1, 1, 'Pilot', '2008-09-09')
show.add_episode(1, 2, 'The Same Old Story', '2008-09-16')

show.add_season(2)
show.add_episode(2, 1, "A New Day in the Old Town", "2009-09-17")
show.add_episode(2, 2, "Night of Desirable Objects", "2009-09-24")

show.write_out('/Users/fmuller/git-work/private/wikipedia_tvshow_scraper/temp')



# URL = "https://en.wikipedia.org/w/api.php"

# keyword = 'Friends'

# SRSEARCH = "intitle:" + keyword + "+incategory:English-language_television_shows"

# PARAMS = {
#     "action": "query",
#     "list": "search",
#     "srsearch": SRSEARCH,
#     "format": "json"
# }

# PARAMS_STR = "&".join(f"{k}={v}" for k,v in PARAMS.items())

# r = requests.get(url=URL, params=PARAMS_STR)

# data = r.json()

# titles = [d['title'] for d in data['query']['search']]

# print(titles)

