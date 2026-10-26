from django import forms
from django.contrib.auth.models import User
from cards.models import FlashcardSet, Flashcard


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        widget=forms.TextInput(attrs={'autofocus': True})
    )

class SetSettingsForm(forms.ModelForm):
    class Meta:
        model = FlashcardSet
        fields = ['title', 'published', 'category', 'description']

class FlashcardAddForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['term', 'definition']

    def __init__(self, *args, **kwargs):
        self.flashcard_set = kwargs.pop('flashcard_set', None)
        super().__init__(*args, **kwargs)

        self.fields['term'].widget.attrs.update({'autofocus': 'autofocus'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.flashcard_set:
            instance.set = self.flashcard_set
        if commit:
            instance.save()
        return instance

class FlashcardSetCreateForm(forms.ModelForm):
    class Meta:
        model = FlashcardSet
        fields = ['title', 'category', 'description']