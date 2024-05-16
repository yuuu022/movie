from django.shortcuts import redirect, render
from mymovie.models import Member_data, Ticket, Movie, Staff_data


# Manager
# 新增電影
def addMovie(request):
    CHOICES = ('即將上映', '現正熱映')
    if request.method=='POST':
        movie_no = request.POST.get('movie_no')
        movie_name = request.POST.get('movie_name')
        date = request.POST.get('date')
        show = request.POST.get('show')
        director = request.POST.get('director')
        actor = request.POST.get('actor')
        type = request.POST.get('type')
        length = request.POST.get('length')
        picture = request.POST.get('picture')
        staff_data_instance = Staff_data.objects.get(staff_no=1)
        Movie.objects.create(
            movie_no=movie_no,
            movie_name=movie_name,
            date=date,
            show=show,
            director=director,
            actor=actor,
            type=type,
            length=length,
            picture=picture,
            change_staff = staff_data_instance
            )
        message='電影新增成功'
        return render(request, 'manager_showMovie.html',locals())
    else:
        return render(request, 'manager_addMovie.html',locals())

# 刪除電影
def deleteMovie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        return render(request,'manager_searchMovie.html',locals()) #<-  電影編輯頁面
    return render(request, 'manager_deleteMovie.html', {'movie': movie})

# 編輯電影
from .forms import MovieForm
def editMovie(request, movie_id):
    CHOICES = ('即將上映', '現正熱映','下架電影')
    if Movie.objects.filter(movie=movie_id).exists():
        movie_instance = Movie.objects.get(movie=movie_id)
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie_instance)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = MovieForm(instance=movie_instance)
        return render(request, 'manager_editMovie.html', {'form': form, 'movie_instance': movie_instance})
    else:
        return redirect('/')
    
# 顯示電影
def showMovie(request, movie_id):
    movie = Movie.objects.all()
    return render(request, 'manager_showMovie.html', locals())

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
    return render(request, 'manager_searchMovie.html', locals())

# request.method == "POST" 用於處理需要提交資料並可能修改伺服器狀態的請求(處理表單提交等資料的傳送)
# request.method == "GET"  用於從伺服器獲取資源的請求，且通常用於獲取較小且不敏感的資料。

# 會員資料
def searchMember(request):
    members = Member_data.objects.all()
    memberFilter = MemberFilter(queryset=members)
    if request.method == "POST":
        memberFilter = MemberFilter(request.POST, queryset=members)
    context = {
        'memberFilter': memberFilter
    }
    return render(request, 'manager_searchMember.html', locals())

def searchMemberDetails(request):
    members = Member_data.objects.all()
    memberFilter = MemberFilter(queryset=members)
    if request.method == "POST":
        memberFilter = MemberFilter(request.POST, queryset=members)
    context = {
        'memberFilter': memberFilter
    }
    return render(request, 'manager_searchMemberDetails.html', locals())    
#---------------------------------------------------------------------------------------------------------------
# User

# 電影資訊
# def movieInformation(request,movie_id)

# 快速購票



# 會員資訊****
from django.http import Http404
from django.contrib.auth.decorators import login_required
# @login_required
def lookMember(request, member_id):
    try:
        member = Member_data.objects.get(member_no=member_id)
    except Member_data.DoesNotExist:
        raise Http404("Member does not exist")
    
    if member.member_account != request.user:  # 这里假设成员的账户与当前登录用户的账户不匹配
        raise Http404("You are not authorized to view this member")
    context = {'lookMember': member}
    return render(request, 'user_lookMember_user.html', context)
