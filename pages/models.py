from django.db import models


class BaseModel(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}: {self.title}"


class Content(BaseModel):
    counter = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Video(Content):
    video_file_link = models.URLField()
    subtitles_file_link = models.URLField()

    def __str__(self):
        return f"Видео {super().__str__()}"


class Audio(Content):
    bit_rate = models.PositiveIntegerField()

    def __str__(self):
        return f"Аудио {super().__str__()}"


class Text(Content):
    body = models.TextField()

    def __str__(self):
        return f"Текст {super().__str__()}"


class Page(BaseModel):
    videos = models.ManyToManyField(Video, related_name="pages")
    audios = models.ManyToManyField(Audio, related_name="pages")
    texts = models.ManyToManyField(Text,related_name="pages")

    def __str__(self):
        return f"Страница {super().__str__()}"
