from django.contrib import admin

from .models import MyHabit

# Register your models here.


@admin.register(MyHabit)
class MyHabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'action', 'is_pleasanthabit', 'is_publichabit',)
    list_filter = ('is_pleasanthabit', 'is_publichabit',)
    search_fields = ('name', 'owner__email', 'owner__tg_nickname', )
    ordering = ('date_begin', 'id',)