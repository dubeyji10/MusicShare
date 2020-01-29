from django import forms
from django.contrib.auth.models import User

from .models import Album, Songs

# class UserForm(forms.ModelForm):

#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']


class SongsForm(forms.ModelForm):
    def form_valid(self, form):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        form.instance.album = album
        return super(self).form_valid(form)
    class Meta:
        model = Songs
        fields = ['song_title','audio_file','lyrics']

class SearchForm(forms.Form):
    query=forms.CharField()