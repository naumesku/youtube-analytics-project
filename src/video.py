from src.channel import Channel
from googleapiclient.discovery import build

class Video(Channel):

    def __init__(self, video_id) -> None:
        self.video_id = video_id
        try:
            self.video_response = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.video_id
                                                         ).execute()
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']
        except IndexError:
            print('Не верно задаано ID vidio.')
            self.video_response = None
            self.title: str = None
            self.view_count: int = None
            self.like_count: int = None
            self.comment_count: int = None

    def __str__(self) -> str:
        return str(f"{self.title}")

class PLVideo(Video):
    def __init__(self, video_id, playlist_id) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

# video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
# print(video2.like_count)
