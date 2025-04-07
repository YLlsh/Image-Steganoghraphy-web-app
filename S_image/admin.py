from django.contrib import admin
from .models import *

@admin.register(EncryptedHistory)
class AllAdmin(admin.ModelAdmin):
    list_display = ('user', 'E_image', 'E_date')  
    search_fields = ('user',) 
    list_filter = ('E_date',)  
