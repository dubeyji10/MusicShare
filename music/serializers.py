from rest_framework import serializers
from .models import Songs,Album


class AlbumSerializer(serializers.ModelSerializer):
       #try using serializers.HyperlinkedModelSerializer
    songs = serializers.StringRelatedField(many=True)
    class Meta:
        model = Album
        fields = ('title','artists','genre','date_posted','author','image','songs')


class SongsSerializer(serializers.ModelSerializer):
   # album = serializers.StringRelatedField(many=True)
    class Meta:
        model = Songs
        fields  = ('song_title','lyrics','audio_file','created_date')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
        # albums not passed therefore not linked with albums now