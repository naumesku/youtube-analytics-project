import datetime
import isodate
from src.video import Video

class PlayList(Video):
    def __init__(self, playlist_id) -> None:
        self.playlist_id = playlist_id
        self.playlist_videos_data = self.get_service().playlists().list(id=self.playlist_id, part='snippet').execute()
        self.title = self.playlist_videos_data['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_videos_data['items'][0]['id']}"
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()

    @property
    def total_duration(self):
        """возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        duration_sum = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_sum += duration
        return duration_sum

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        like_count_max = 0
        videoId_best = ''
        for video_data in self.playlist_videos['items']:
            videoId = video_data['contentDetails']['videoId']
            like_count = Video(videoId).like_count
            if int(like_count) > like_count_max:
                like_count_max = int(like_count)
                videoId_best = videoId
        return f"https://youtu.be/{videoId_best}"
