from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from jalali_date import datetime2jalali, date2jalali


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', '_session_data', 'get_expire_date', 'get_expire_time']
    readonly_fields = ['_session_data']

    def _session_data(self, obj):
        return obj.get_decoded()

    @admin.display(description='تاریخ انقضاء')
    def get_expire_date(self, obj):
        return date2jalali(obj.expire_date)

    @admin.display(description='تاریخ انقضاء')
    def get_expire_time(self, obj):
        return datetime2jalali(obj.expire_date).strftime('%H:%M')


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'get_action_date', 'get_action_time', 'action_flag']
    list_filter = ['action_time']
    search_fields = ['user__phone_number']

    @admin.display(description='زمان اقدام')
    def get_action_date(self, obj):
        return date2jalali(obj.action_time)

    @admin.display(description='زمان اقدام')
    def get_action_time(self, obj):
        return datetime2jalali(obj.action_time).strftime('%H:%M')
