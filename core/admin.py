from django.contrib import admin
from .models import HeroSlide, Advantage, SupportTicket

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active')
    list_editable = ('order', 'active')
    search_fields = ('title', 'subtitle')
    ordering = ('order',)

@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'active')
    list_editable = ('icon', 'order', 'active')
    search_fields = ('title', 'description')
    ordering = ('order',)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'topic', 'status', 'created_at')
    list_filter = ('status', 'topic', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'email', 'topic', 'status')
        }),
        ('Сообщение', {
            'fields': ('message', 'response')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
