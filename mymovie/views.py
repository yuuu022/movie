from django.shortcuts import get_object_or_404, redirect, render
from mymovie.models import Member_data, Ticket, Movie, Staff_data, Session

# 首頁
def home(request):
    return render(request, 'base.html')

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
        movie = Movie.objects.create(
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
        return redirect('addSession')
    else:
        return render(request, 'manager_addMovie.html',locals())
    
# 新增場次
def addSession(request):
    if request.method == 'POST':
        movie_id = request.POST['movie']
        session_desc = request.POST['session']
        movie = get_object_or_404(Movie, pk=movie_id)
        session = Session(movie=movie, session=session_desc)
        session.save()
        return redirect('showMovie', movie_no=movie.pk)
    else:
        movies = Movie.objects.all()
        return render(request, 'manager_addSession.html', {'movies': movies})

# 刪除電影
def deleteMovie(request, movie_no):
    if movie_no:
        try:
            movie = Movie.objects.get(movie_no=movie_no)
            movie.delete()
        except:
            pass
    return redirect('searchMovie')

# 編輯電影
from .forms import MovieForm   
def editMovie(request, movie_no):
    movie_instance = get_object_or_404(Movie, movie_no=movie_no)    
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie_instance)
        if form.is_valid():
            form.save()
            return redirect('showMovie', movie_no=movie_instance.movie_no)
    else:
        form = MovieForm(instance=movie_instance)
    context = {
        'form': form,
        'movie_instance': movie_instance,
    }
    return render(request, 'manager_editMovie.html', context) 
    
# 搜尋電影
from .filters import MovieFilter,MemberFilter
def searchMovie(request):
    movies = Movie.objects.all()
    movieFilter = MovieFilter(request.GET, queryset=movies)
    context = {
        'movieFilter': movieFilter
    }
    return render(request, 'manager_searchMovie.html', context)

# 顯示電影
def showMovie(request, movie_no):
    movie = Movie.objects.get(movie_no=movie_no)
    ses = Session.objects.filter(movie=movie_no)
    return render(request, 'manager_showMovie.html', locals())
# request.method == "POST" 用於處理需要提交資料並可能修改伺服器狀態的請求(處理表單提交等資料的傳送)
# request.method == "GET"  用於從伺服器獲取資源的請求，且通常用於獲取較小且不敏感的資料。

# 會員購票紀錄
def search_member_info(member_no):
    try:
        member = Member_data.objects.get(member_no=member_no)
        # 會員的訂票
        tickets = Ticket.objects.filter(ticket_member=member)
        # 字典
        result = {
            'member_account': member.member_account,
            'gmail': member.gmail,
            'phone_number': member.phone_number,
            'tickets': [],
        }
        # 定義 payment_method 
        payment_method_display = {
            'money': '現金',
            'credit_card': '信用卡'
        }
        for ticket in tickets:
            session = Session.objects.get(pk=ticket.session_id_id)
            movie = session.movie
            result['tickets'].append({
                'session': session.session,
                'movie_name': movie.movie_name,
                'ticket_amount': ticket.ticket_amount,
                'payment_method': payment_method_display.get(ticket.payment_method, ticket.payment_method)
            })
        return result
    except Member_data.DoesNotExist:
        return None

def searchTicket(request):
    member_info = None
    if request.method == 'POST':
        member_no = request.POST.get('member_no')
        if member_no:
            member_info = search_member_info(member_no)
    return render(request, 'manager_searchTicket.html', {'member_info': member_info})

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



# 查看會員資訊
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
@login_required
def login_view(request):
    if request.method == 'POST':
        member_account = request.POST['member_account']
        member_password = request.POST['member_password']
        user = authenticate(request, username=member_account, password=member_password)
        if user is not None:
            login(request, user)
            return redirect('user_lookMember')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')

@login_required
def lookMember(request):
    member = Member_data.objects.get(member_account=request.user.username)
    return render(request, 'user_lookMember.html', {'member': member})

# 編輯會員




