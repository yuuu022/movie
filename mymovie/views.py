
from django.shortcuts import get_object_or_404, redirect, render
from .models import Member_data, Ticket, Movie, Staff_data, Session

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
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html')

def lookMember(request):
    try:
        member_id = request.session.get('member_id')
        if not member_id:
            return redirect('/loginMember/')
        
        member = Member_data.objects.get(member_account=member_id)
        return render(request, 'user_lookMember.html', {'member': member})
    except Member_data.DoesNotExist:
        return redirect('/loginMember/')

# 編輯會員
from django.contrib.auth.decorators import login_required
from .forms import MemberEditForm
def editMember(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('/loginMember/')
    
    try:
        member = Member_data.objects.get(member_account=member_id)
    except Member_data.DoesNotExist:
        return redirect('/loginMember/')
    
    if request.method == 'POST':
        form = MemberEditForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/lookMember/')
    else:
        form = MemberEditForm(instance=member)
    
    return render(request, 'user_editMember.html', {'form': form})



from .forms import MemberRegisterForm, MemberLoginForm
from django.contrib.auth.hashers import make_password

#會員註冊
def registerMember(request):
    if request.method == 'POST':
        register_form = MemberRegisterForm(request.POST)
        if register_form.is_valid():
            member_id = register_form.cleaned_data['member_id'].strip()
            member_pw = register_form.cleaned_data['member_pw']
            member_pwc = register_form.cleaned_data['member_pwc']
            member_mail = register_form.cleaned_data['member_mail']
            member_phone = register_form.cleaned_data['member_phone']
            
            if member_pw == member_pwc:
                if not Member_data.objects.filter(member_account=member_id).exists():
                    pw = make_password(member_pw)
                    member = Member_data.create_member_data(member_id, pw, member_mail, member_phone)
                    member.save()
                    message = "註冊成功! 請點選「會員中心」進行登入"
                else:
                    message = "帳號已經存在"
            else:
                message = "密碼不一致"
        else:
            message = "請檢查輸入的欄位內容"
    else:
        register_form = MemberRegisterForm()
    return render(request, 'user_register.html', locals())

from django.contrib.auth.hashers import check_password
#-------------------------------------------------------------------------------------------------------------
#會員登入
#-------------------------------------------------------------------------------------------------------------
def loginMember(request):
    if request.method == 'GET':
        form = MemberLoginForm()
        return render(request, 'user_login.html', {'form': form})
         
    elif request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data['member_id'].strip()
            member_pw = form.cleaned_data['member_pw']
            print(f'member_id:{member_id}, password: {member_pw}')
            try:
                member = Member_data.objects.get(member_account=member_id)
                if check_password(member_pw, member.member_password):
                    # 这里没有使用 Django 内置的用户系统，手动登录
                    request.session['member_id'] = member_id
                    message = '成功登入了'
                    return redirect('/lookMember/')
                else:
                    message = '登入失敗'
            except Member_data.DoesNotExist:
                message = '沒有此帳號'
        else:
            message = '表單內容有誤'
        return render(request, 'user_login.html', {'form': form, 'message': message})
    else:
        message = '錯誤的請求方法'
    return render(request, 'user_login.html', {'form': form, 'message': message})
#-------------------------------------------------------------------------------------------------------------
#會員忘記密碼
#-------------------------------------------------------------------------------------------------------------
from .forms import MemberForgetForm

def forgetMember(request):
    if request.method == 'POST':
        form = MemberForgetForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data['member_id'].strip()
            member_pw = form.cleaned_data['member_pw']
            member_cpw = form.cleaned_data['member_cpw']
            if member_pw == member_cpw:
                try:
                    member = Member_data.objects.get(member_account=member_id)
                    member.member_password = make_password(member_pw)
                    member.save()
                    message = "成功更改密碼 請重新登入"
                    #return redirect('/loginMember/')
                except Member_data.DoesNotExist:
                    message = "此帳號不存在"
            else:
                message = "新密碼與確認新密碼不一致"
        else:
            message = "表單內容有誤"
        return render(request, 'user_forget.html', {'form': form, 'message': message})
    else:
        form = MemberForgetForm()
    return render(request, 'user_forget.html', {'form': form})


from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('/loginMember/')


from .forms import ManagerRegisterForm, ManagerLoginForm, ManagerForgetForm
#-------------------------------------------------------------------------------------------------------------
#員工註冊
#-------------------------------------------------------------------------------------------------------------
def registerManager(request):
    CHOICES = (
        ('it', 'IT部門'),
        ('hr', '人事部門')
    )    
    message =""
    if request.method == 'POST':
        register_form = ManagerRegisterForm(request.POST)
        if register_form.is_valid():
            manager_id = register_form.cleaned_data['manager_id'].strip()
            manager_department = register_form.cleaned_data['manager_department']
            manager_pw = register_form.cleaned_data['manager_pw']
            manager_pwc = register_form.cleaned_data['manager_pwc']
            
            if manager_pw == manager_pwc:
                if not Staff_data.objects.filter(staff_no=manager_id).exists():
                    pw = make_password(manager_pw)
                    manager = Staff_data.create_manager_data(manager_id, pw, manager_department)
                    manager.save()
                    message = "註冊成功! 請點選「會員中心」進行登入"
                else:
                    message = "帳號已經存在"
            else:
                message = "密碼不一致"
        else:
            message = "請檢查輸入的欄位內容"
    else:
        register_form = ManagerRegisterForm()
    return render(request, 'manager_register.html', {'form': register_form, 'message': message, 'CHOICES':CHOICES})
#-------------------------------------------------------------------------------------------------------------
#員工登入
#-------------------------------------------------------------------------------------------------------------
from django.contrib import messages

def loginManager(request):
    if request.method == 'GET':
        form = ManagerLoginForm()
        return render(request, 'manager_login.html', {'form': form})
         
    elif request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            manager_id = form.cleaned_data['manager_id'].strip()
            manager_pw = form.cleaned_data['manager_pw']
            print(f'manager_id:{manager_id}, password: {manager_pw}')
            try:
                manager = Staff_data.objects.get(staff_account=manager_id)
                if check_password(manager_pw, manager.staff_password):
                    # 这里没有使用 Django 内置的用户系统，手动登录
                    request.session['manager_id'] = manager_id
                    message = '成功登入了'
                    return redirect('/searchMovie/')
                else:
                    message = '登入失敗'
            except Staff_data.DoesNotExist:
                message = '沒有此帳號'
        else:
            print(form.errors)
            # message = '表單內容有誤'
            message = '表單內容有誤: {}'.format(form.errors)
        return render(request, 'manager_login.html', {'form': form, 'message': message})
    else:
        message = '錯誤的請求方法'
    return render(request, 'manager_login.html', locals())
#-------------------------------------------------------------------------------------------------------------
#員工忘記密碼
#-------------------------------------------------------------------------------------------------------------
def forgetManager(request):
    if request.method == 'POST':
        form = ManagerForgetForm(request.POST)
        if form.is_valid():
            manager_id = form.cleaned_data['manager_id'].strip()
            manager_pw = form.cleaned_data['manager_pw']
            manager_cpw = form.cleaned_data['manager_cpw']
            if manager_pw == manager_cpw:
                try:
                    manager = Staff_data.objects.get(staff_account=manager_id)
                    manager.staff_password = make_password(manager_pw)
                    manager.save()
                    message = "成功更改密碼 請重新登入"
                    #return redirect('/loginMember/')
                except Staff_data.DoesNotExist:
                    message = "此帳號不存在"
            else:
                message = "新密碼與確認新密碼不一致"
        else:
            message = "表單內容有誤"
        return render(request, 'manager_forget.html', {'form': form, 'message': message})
    else:
        form = ManagerForgetForm()
    return render(request, 'manager_forget.html', locals())

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('/loginMember/')