from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #one to many relationship
from django.urls import reverse
from PIL import Image
from django.db import models
from datetime import timedelta as tdelta
# from django.utils import get_file_upload_path, get_cover_upload_path
import os

class Album(models.Model):
    title = models.CharField(max_length = 100)
    artists = models.TextField()
    genre = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author  = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True,upload_to='album_cover')
    
    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 600:
                output_size = (400,300)
                img.save(self.image.path)


            return self.image.url
        return ''

    def save(self):
        super().save()

    def get_absolute_url(self):
        return reverse('album-detail',kwargs={'pk':self.pk})

    # def approved_comments(self):
    #     return self.comments.filter(approved_comment=True)





class Songs(models.Model):
    album = models.ForeignKey("Album", on_delete=models.CASCADE,related_name = 'songs')
    lyrics = models.TextField()
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='',upload_to='songs')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = u'Songs'

    def get_absolute_url(self):
        return reverse('song-detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.song_title

    @property
    def audio_file_url(self):
        if self.audio_file:
            return self.audio_file.url
        return ''

    def save(self, *args, **kwargs):
        super(Songs, self).save(*args, **kwargs)
        # file_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
        # super(Song, self).save(*args, **kwargs)
    
    def save(self):
        super().save()
