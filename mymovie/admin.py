from django.contrib import admin 
from .models import Member_data, Ticket, Session, Movie, Staff_data
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_no','member_account','gmail','phone_number')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_no','ticket_member','session_id','ticket_amount','payment_method')

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_no','movie','session')

class MovieAdmin(admin.ModelAdmin):
    inlines = [SessionInline]
    list_display = ('movie_no','movie_name','date','show','director','actor','type','length','change_staff')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_no','staff_password','staff_name','staff_department')



admin.site.register(Member_data, MemberAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Staff_data, StaffAdmin)