from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from ..models import FlashcardSet, Flashcard
from ..forms import SetSettingsForm, FlashcardAddForm, FlashcardSetCreateForm


@login_required
def edit_set(request, id):
    try:
        flashcard_set = FlashcardSet.objects.get(pk=id, user=request.user)
    except FlashcardSet.DoesNotExist:
        raise Http404

    flashcards = Flashcard.objects.filter(set=flashcard_set).all()

    context = {
        'set': flashcard_set,
        'cards': flashcard_set.flashcards.exists(),
        'flashcards': flashcards,
    }

    return render(request, "flashcard/set_edit.html", context)

@login_required
def edit_flashcard_set_flashcard(request, set_id, card_id):
    try:
        set = FlashcardSet.objects.get(pk=set_id, user=request.user)
    except FlashcardSet.DoesNotExist:
        raise Http404

    try:
        card = Flashcard.objects.get(pk=card_id, set=set)
    except Flashcard.DoesNotExist:
        raise Http404

    if request.method == "POST":
        raise Http404
    else:
        return render(request, 'flashcard/edit_flashcard.html', {'card': card})

@login_required
def set_settings(request, id):
    try:
        flashcard_set = FlashcardSet.objects.get(pk=id, user=request.user)
    except FlashcardSet.DoesNotExist:
        raise Http404

    settings_form = SetSettingsForm(request.POST or None, instance=flashcard_set)

    if request.method == 'POST':
        if "delete_set" in request.POST:
            flashcard_set.delete()
            return redirect("home")

        if settings_form.is_valid():
            settings_form.save()
            return redirect('edit_set', id)
    else:
        return render(request, 'flashcard/set_settings.html', {'settings_form': settings_form, 'set': flashcard_set})

@login_required
def set_add_card(request, id):
    try:
        flashcard_set = FlashcardSet.objects.get(pk=id, user=request.user)
    except FlashcardSet.DoesNotExist:
        raise Http404

    add_form = FlashcardAddForm(request.POST or None, flashcard_set=flashcard_set)

    if request.method == 'POST':
        if add_form.is_valid():
            add_form.save()
            return redirect('edit_set', id)
    else:
        return render(request, 'flashcard/set_add_card.html', {'form': add_form, 'set': flashcard_set})

@login_required
def set_create_new(request):
    form = FlashcardSetCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            flashcard_set = form.save(commit=False)
            flashcard_set.user = request.user
            flashcard_set.save()
            return redirect('flashcard_set_detail', flashcard_set.id)
    else:
        return render(request, "flashcard/set_create.html", {'form': form})