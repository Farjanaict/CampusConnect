from django.contrib import admin
from .models import Event, EventRegistration, LostFound, Complaint

admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(LostFound)
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'student', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'student__username')