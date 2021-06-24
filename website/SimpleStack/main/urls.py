'''
another urls patterns file. this one is for our app: board
this differs from the first one since it is exclusive for our main app.

'''


from django.urls import path
from . import views


from django.conf.urls import handler404, handler500

urlpatterns = [
    #empty string
    path('', views.home, name='main-home'), #explicit link: "ourmainaddress.com/" <-- home page
    path('about/', views.about, name='main-about'), #explicit link: "ourmainaddress.com/about"
    path('search/', views.search, name='searchbar'),
    path('guide/', views.guide, name='main-guide'),
    path('Legal/', views.legal, name='main-Legal'),
    path('answer/<id>/', views.answer, name='answer'), #click on a title link
    
]


#handler500 = 'main.views.handler500'