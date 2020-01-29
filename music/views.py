from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from .models import Album, Songs
from django.urls import reverse
import os
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from PIL import Image
from .forms import SongsForm,SearchForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic.dates import YearArchiveView,MonthArchiveView,WeekArchiveView
from django.template import loader,Context
from django.http import HttpResponse
from datetime import *
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def welcome(request):
    return render(request,'music/welcome.html',{'title':'Welcome'})

def home(request):
    context = {
        'albums':Album.objects.all()
    }
    return render(request,'muisc/home.html',context)

def about(request):
    return render(request,'music/about.html',{'title': 'About MusicShare'})

def announcement(request):
    return render(request,'music/announcement.html',{'title': 'Announcements' })
    
class AlbumListView(ListView):
    model = Album
    template_name = 'music/home.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = 'albums'
    ordering = ['-date_posted']
    paginate_by = 4


class AlbumDetailView(DetailView):
    model = Album

#delete this view .... 
class AlbumDetailView2(DetailView):
    model = Album

def detail2(request):
    return redirect('album-detail2', pk=song.album.pk)

#adding month view
# class PostMonthArchiveView(MonthArchiveView):
#     queryset = Post.objects.all()
#     date_field = "date_posted"
#     allow_future = True

# def archive(request, year, month):
#     post_list = Post.objects.filter(date_posted__year=year,date_posted__month=month).order_by('-date_posted')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class UserAlbumListView(ListView):
    model = Album
    template_name = 'music/user_albums.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = 'albums'
    #ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Album.objects.filter(author=user).order_by('-date_posted')
        
class AlbumCreateView(LoginRequiredMixin,CreateView):
    model = Album
    fields = ['title','genre','artists','image']

    def form_valid(self,form):
        #setting the author to the logged in
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class AlbumUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['title','genre','artists','image']

    def form_valid(self,form):#setting the author to the logged in
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        album = self.get_object()
        if self.request.user == album.author:
            return True
        return False #403 -forbidden 

class AlbumDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Album
    success_url = '/home'
    def test_func(self):
        album = self.get_object()
        if self.request.user == Album.author:
            return True
        return False #403 -forbidden 

def delete_album(request, pk):
    
    album = Album.objects.get(pk=pk)
    album.delete()
    albums = Album.objects.filter(user=request.author)
    return render(request, 'music/home.html', {'albums': albums})



class SearchView(ListView):
    model = Album
    template_name = 'music/search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('q')
       if query:
          albumresult = Album.objects.filter(title__contains=query)
          result = albumresult
       else:
           result = None
       return result


#
# class SearchView(TemplateView):
#     template_name = 'blog/search.html'
#     model = Post
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list= Post.objects.filter(Q(title__icontains='q'))
#         return object_list

#----------------------------------------------------------------------------


@login_required
def add_songs_to_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == "POST":
        form = SongsForm(request.POST or None, request.FILES or None)
        #form = SongsForm(request.POST)
        if form.is_valid():
            songs = form.save(commit=False) #False .. default
            songs.album = album
            songs.audio_file = request.FILES['audio_file']
            songs.save()
            return redirect('album-detail', pk=album.pk)
    else:
        form = SongsForm()
    return render(request, 'music/add_songs_to_album.html', {'form': form})


# @login_required
# def add_songs_to_album(request, pk): #pk so --
#     form = SongsForm(request.POST or None, request.FILES or None)
#     album = get_object_or_404(Album, pk=pk) #-- not album.pk use pk=pk
#     if form.is_valid():
#         Song = form.save(commit=False)
#         Song.album = album
#         Song.audio_file = request.FILES['audio_file']
#         file_type = Song.audio_file.url.split('.')[-1]
#         file_type = file_type.lower()
#         if file_type not in AUDIO_FILE_TYPES:
#             context = {
#                 'album': album,
#                 'form': form,
#                 'error_message': 'Audio file must be WAV, MP3, or OGG',
#             }
#             return render(request, 'music/add_songs_to_album.html', context)
#         Song.save()
#         return render(request, 'music/album_detail.html', {'album': album})
#     context = {
#         'album': album,
#         'form': form,
#     }
#     return render(request, 'music/add_songs_to_album.html', context)

# @login_required
# def song_remove(request, pk):
#     song = get_object_or_404(Songs, pk=pk)
#     song.delete()
#     return redirect('album-detail', pk=song.album.pk)

@login_required
def song_delete(request, pk):
    song = get_object_or_404(Songs, pk=pk)
    song.delete()
    return redirect('album-detail', pk=song.album.pk)

class SongRemoveView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Songs
    success_url = 'album-detail'
    def test_func(self):
        song = self.get_object()
        if self.request.user == song.author:
            return True
        return False #403 -forbidden 

def latest_albums(request):
    latest_Album = Album.objects.all()
    #page = request.GET.get('page')
    forms = Album.objects.filter(date_posted__lte=timezone.now()).order_by('-date_posted')[0:3]
    #paginator = Paginator(post_list, per_page=3)
    return render(request, 'music/latest_album.html', {'album': latest_albums,'forms': forms,})


def listallusers(request):
    all_users = User.objects.all()
    #page = request.GET.get('page')
    #forms = Post.objects.filter(date_posted__lte=timezone.now()).order_by('-date_posted')[0:3]
    #paginator = Paginator(post_list, per_page=3)
    return render(request, 'music/AllUsers.html', {'all_users': all_users,})


def favorite(request, song_id):

    song = get_object_or_404(Songs, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Songs.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):

    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

