"""
URL configuration for movie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mymovie import views as mv


urlpatterns = [
    path('admin/', admin.site.urls),
    # 註冊、登入、忘記密碼
    # path('/',mv. , name=''),


    #-----------------------------------------------------------
    # Manager
    # 電影處理
    path('addMovie/',mv.addMovie , name='addMovie'),
    path('editMovie/<int:movie_id>/', mv.editMovie, name='editMovie'),
    path('deleteMovie/<int:movie_id>/',mv.deleteMovie , name='deleteMovie'),
    path('searchMovie/',mv.searchMovie , name='searchMovie'),
    path('showMovie/<int:movie_id>/',mv.showMovie , name='showMovie'),
    # path('/',mv. , name=''),


    # 會員購票紀錄
    # path('/',mv. , name=''),

    # 會員資料
    path('lookMember/<int:member_id>/',mv.lookMember, name='lookMember'),
    path('searchMemberDetails/',mv.searchMemberDetails, name='searchMemberDetails'),
    


    #-----------------------------------------------------------
    # User
    # 電影資訊
	# path('movieInformation/',mv.movieInformation, name='movieInformation'),


    # 快速購票


    # 會員中心


]
