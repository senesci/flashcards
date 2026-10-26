from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from ..models import FlashcardSet, Category, Flashcard
from django.contrib.auth.models import User

from ..forms import SearchForm


def flashcard_set_detail(request, id):
    try:
        flashcard_set = get_flashcard_set(request, id)
    except FlashcardSet.DoesNotExist:
        raise Http404

    if not flashcard_set:
        raise Http404

    related = FlashcardSet.objects.filter(category=flashcard_set.category, user__is_active=True, published=True).exclude(id=flashcard_set.id)[:6]
    cards = Flashcard.objects.filter(set=flashcard_set)

    context = {
        'set': flashcard_set,
        'related': related,
        'cards': cards,
    }

    return render(request, "flashcard/set_detail.html", context)


def flashcard_set_quiz(request, id):
    flashcard_set = get_flashcard_set(request, id)

    if not flashcard_set:
        raise Http404

    cards = list(Flashcard.objects.filter(set=flashcard_set).values('term', 'definition'))

    context = {
        'set': flashcard_set,
        'cards': cards,
    }

    return render(request, "flashcard/quiz.html", context)


def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        raise Http404

    sets = FlashcardSet.objects.filter(category=category, user__is_active=True, published=True).all()

    context = {
        'category': category,
        'sets': sets,
    }
    return render(request, "category/detail.html", context)

def get_flashcard_sets(request, target_user):
    if request.user == target_user:
        return FlashcardSet.objects.filter(user=target_user, user__is_active=True).order_by("-id")
    else:
        return FlashcardSet.objects.filter(user=target_user, published=True, user__is_active=True).order_by("-id")

def get_flashcard_set(request, id):
    flashcard_set = get_object_or_404(FlashcardSet, id=id, user__is_active=True)

    if flashcard_set.user == request.user or flashcard_set.published:
        return flashcard_set

    return None

def user_profile_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    if not user.is_active:
        raise Http404

    flashcard_sets = get_flashcard_sets(request, user)

    context = {
        "sets": flashcard_sets,
        "account": user,
    }

    return render(request, "user/profile.html", context)


def search_view(request):
    flashcard_sets = None
    search_performed = False

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_performed = True
            query = form.cleaned_data['query']
            flashcard_sets = FlashcardSet.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(user__username__icontains=query),
                user__is_active=True,
                published=True
            )
    else:
        form = SearchForm()

    return render(request, "search.html", {
        'form': form,
        'sets': flashcard_sets,
        'search_performed': search_performed
    })


def custom_404_view(request, exception):
    return render(request, "errors/resource.html")