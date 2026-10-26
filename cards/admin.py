from django.contrib import admin
from .models import Category, FlashcardSet, Flashcard, FlashcardReview
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

class QuizAdminSite(admin.AdminSite):
    site_header = "Quiz Admin"
    site_title = "Quiz Admin"
    index_title = "Manage users, flashcards, and other data."

quiz_admin= QuizAdminSite(name='quizadmin')

class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('term', 'definition_preview', 'set', 'created_at')
    list_filter = ('set',)
    search_fields = ('term', 'definition', 'set__title')

    def definition_preview(self, obj):
        return obj.definition[:50] + "…" if len(obj.definition) > 50 else obj.definition
    definition_preview.short_description = "Definition Preview"

quiz_admin.register(Flashcard, FlashcardAdmin)
quiz_admin.register(Category)
quiz_admin.register(FlashcardSet)
quiz_admin.register(FlashcardReview)

quiz_admin.register(User, UserAdmin)
quiz_admin.register(Group, GroupAdmin)