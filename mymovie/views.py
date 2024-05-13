from django.shortcuts import redirect, render
from mymovie.models import Member_data, Ticket, Movie, Staff_data


# Manager

# 新增電影
def addMovie(request):
    if request.method=='POST':
        movie = request.POST.get('movie')
        movie_name = request.POST.get('movie_name')
        date = request.POST.get('date')
        show = request.POST.get('show')
        director = request.POST.get('director')
        actor = request.POST.get('actor')
        type = request.POST.get('type')
        length = request.POST.get('length')
        picture = request.POST.get('picture')
        change_staff = request.POST.get('change_staff')
        Movie.objects.create(
            movie=movie,
            movie_name=movie_name,
            date=date,
            show=show,
            director=director,
            actor=actor,
            type=type,
            length=length,
            picture=picture,
            change_staff=change_staff)
        message='電影新增成功'
    else:
        return render(request, 'addMovie.html',locals())

# 刪除電影
def deleteMovie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect(' ') #<-  電影編輯頁面
    return render(request, 'deleteMovie.html', {'movie': movie})

# 編輯電影
from .forms import MovieForm
def editMovie(request, movie_id):
    if Movie.objects.filter(movie=movie_id).exists():
        movie_instance = Movie.objects.get(movie=movie_id)
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie_instance)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = MovieForm(instance=movie_instance)
        return render(request, 'editMovie.html', {'form': form, 'movie_instance': movie_instance})
    else:
        return redirect('/')

# 搜尋電影
from .filters import MovieFilter,MemberFilter

def searchMovie(request):
    movies = Movie.objects.all()
    movieFilter = MovieFilter(queryset=movies)
    if request.method == "POST":
        movieFilter = MovieFilter(request.POST, queryset=movies)
    context = {
        'movieFilter': movieFilter
    }
    return render(request, 'searchMovie.html', locals())

# request.method == "POST" 用於處理需要提交資料並可能修改伺服器狀態的請求(處理表單提交等資料的傳送)
# request.method == "GET"  用於從伺服器獲取資源的請求，且通常用於獲取較小且不敏感的資料。

# 會員中心
def searchMember(request):
    members = Member_data.objects.all()
    memberFilter = MemberFilter(queryset=members)
    if request.method == "POST":
        memberFilter = MemberFilter(request.POST, queryset=members)
    context = {
        'memberFilter': memberFilter
    }
    return render(request, 'manager_searchMember.html', locals())


#---------------------------------------------------------------------------------------------------------------
# User

# 電影資訊
# def movieInformation(request,movie_id)

# 快速購票
