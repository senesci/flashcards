from django.shortcuts import render
from ..models import FlashcardSet, Category


def homepage(request):
    flashcard_sets = FlashcardSet.objects.filter(user__is_active=True, published=True).all()[:6]
    categories = Category.objects.all()

    context = {
        'flashcard_sets': flashcard_sets,
        'categories': categories,
    }

    if not request.user.is_authenticated:
        return render(request, 'index.html', context)
    else:
        return render(request, "home.html", context)
