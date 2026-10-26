from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from cards.forms import UserProfileForm


@login_required
def user_settings_view(request):
    user = request.user

    if request.method == "POST":
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)

            if profile_form.is_valid():
                profile_form.save()
                return redirect('user_settings')

        elif 'change_password' in request.POST:
            profile_form = UserProfileForm(instance=user)
            password_form = PasswordChangeForm(user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('user_settings')

        elif 'delete_account' in request.POST:
            user.delete()
            logout(request)
            return redirect('home')

    else:
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, "user/settings.html", {
        "profile_form": profile_form,
        "password_form": password_form,
    })