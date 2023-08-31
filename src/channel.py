import json
import os
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    object_API = "youtube"

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.channel_data = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.json_data = json.dumps(self.channel_data, indent=2, ensure_ascii=False)

        self.title = json.loads(self.json_data)["items"][0]['snippet']['title']
        self.description = json.loads(self.json_data)["items"][0]['snippet']['description']
        self.url = f"{'https://www.youtube.com/channel/'}{channel_id}"
        self.subscriberCount = json.loads(self.json_data)["items"][0]["statistics"]["subscriberCount"]
        self.video_count = json.loads(self.json_data)["items"][0]["statistics"]["videoCount"]
        self.viewCount = json.loads(self.json_data)["items"][0]["statistics"]["viewCount"]

        # def __repr__(self) -> str:
        #     return f"{self.__class__.__name__}('{self.name}', {self.price}, {self.quantity})"

    def __str__(self) -> str:
        return str(f"{self.title}({self.url})")

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.json_data)
    #
    @classmethod
    def get_service(cls):
        return build(cls.object_API, 'v3', developerKey=cls.api_key)

    def to_json(self, name_file_jonson: str):
        with open(name_file_jonson, "a", encoding='UTF-8') as file:
            json.dump(self.channel_data, file)

    @property
    def channel_id(self):
        return self.__channel_id

    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __lt__(self, other):
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other):
     return self.subscriberCount <= other.subscriberCount

    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        return self.subscriberCount >= other.subscriberCount
