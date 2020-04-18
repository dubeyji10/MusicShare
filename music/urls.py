# from django.urls import path
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls import url
# from django.urls import reverse
# app_name = 'music'
# urlpatterns = [

#     path('welcome/',views.welcome,name='welcome'),#remove this line just checking something

# ]

# if settings.DEBUG:
#     urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
#     urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


from django.urls import path
from .views import AlbumListView,AlbumDetailView,AlbumCreateView,AlbumUpdateView,AlbumDeleteView,UserAlbumListView,SearchView,AlbumDetailView2,SongDetailView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView
from .models import Album
from django.urls import reverse
from music.views import AlbumListView2, SongsListView2

urlpatterns = [

    path('',views.welcome,name='MusicShare'),#remove this line just checking something
    path('home/',AlbumListView.as_view(),name='music-home'),#homepage now
                 #calls home function
    path('about/',views.about,name='music-about'),#.../about
             #call about function
    #
    # path('jsonview/',AlbumDetailView2.as_view(),name='music-jsonview'),#.../about
    url(r'^jsonview/$', AlbumListView2.as_view(),name='jsonview'),
    url(r'^jsonview2/$', SongsListView2.as_view(),name='jsonview2'),
    #
    path('announcemnet/',views.announcement,name='music-announcemnet'),#another simple page
    path('album/<int:pk>/',AlbumDetailView.as_view(),name = 'album-detail'), #uncomment this line
    #path('album/<int:pk>/',views.detail2,name = 'album-detail2'),

            #pk - primary key int-integer type
    path('album/new/',AlbumCreateView.as_view(),name = 'album-create'),
    path('album/<int:pk>/update',AlbumUpdateView.as_view(),name = 'album-update'),
    #path('album/<int:pk>/delete/',AlbumDeleteView.as_view(),name = 'album-delete'),
    path('album/<int:pk>/delete/',views.delete_album,name = 'album-delete'),
    path('album/<int:pk>/song/', views.add_songs_to_album, name='add_songs_to_album'),
    path('song/<int:pk>/remove/', views.song_delete, name='song_delete'),
    #path('search/',views.searchposts,name="post_search"),  
    #add path for /accounts  
    path('user/<str:username>',UserAlbumListView.as_view(),name='user-albums'),
    #path('archive/<int:year>/month/<int:month>', PostMonthArchiveView.as_view(month_format='%m'), name='post_archive_month'),
    #path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('archive/',ArchiveIndexView.as_view(model=Album, date_field="date_posted"),name="archives"),
    path('latest_albums/',views.latest_albums,name='latest-albums'),
    path('allusers/',views.listallusers,name='allusers'),
    url(r'^search/$', SearchView.as_view(), name='search'),#added 17nov
    #path('search/', SearchResultsView.as_view(), name='search_results'),
    #url(r'^search/', views.search, name="search")
    #url(r'^searchform/$', views.searchform),
    #url(r'^search/$', views.search),
    path('song/<int:pk>/lyrics/', views.song_detail2, name='song_detail2'),
    path('song/<int:pk>/',SongDetailView.as_view(),name = 'song-detail'), #uncomment this line


]


if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)