from django.contrib import admin

from pages.models import Page, Video, Audio, Text


class VideoInline(admin.TabularInline):
    model = Page.videos.through
    extra = 1
    can_delete = True
    show_change_link = True
    verbose_name = "Видео"
    verbose_name_plural = "Видео"


class AudioInline(admin.TabularInline):
    model = Page.audios.through
    extra = 1
    can_delete = True
    show_change_link = True
    verbose_name = "Аудио"
    verbose_name_plural = "Аудио"


class TextInline(admin.TabularInline):
    model = Page.texts.through
    extra = 1
    can_delete = True
    show_change_link = True
    verbose_name = "Текст"
    verbose_name_plural = "Тексты"


class PageAdmin(admin.ModelAdmin):

    inlines = [
        VideoInline,
        AudioInline,
        TextInline,
    ]
    exclude = ('videos', 'audios', 'texts',)
    search_fields = ('title',)


class Searchable(admin.ModelAdmin):
    search_fields = ('title',)


admin.site.register(Video, Searchable)
admin.site.register(Audio, Searchable)
admin.site.register(Text, Searchable)
admin.site.register(Page, PageAdmin)
