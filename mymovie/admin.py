from django.contrib import admin 
from .models import Member_data, Ticket, Session, Movie, Staff_data
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ('member','member_account','gmail','phone_number')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('number','ticket_member','session_id','ticket_amount','payment_method')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_number','movie','session')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie','movie_name','date','show','director','actor','type','length','change_staff')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff','staff_password','staff_name','staff_department')



admin.site.register(Member_data, MemberAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Staff_data, StaffAdmin)