"""
URL configuration for flashcards project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.index.html, name='index.html')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='index.html')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from cards.views import home, auth, public, user, set
from cards.admin import quiz_admin

from django.conf.urls import handler404

handler404 = 'cards.views.public.custom_404_view' # ignore the 'unused' warnings

urlpatterns = [
    path('admin/', quiz_admin.urls),
    path("", home.homepage, name="home"),
    path("accounts/login/", auth.login_view, name="login"),
    path("accounts/signup/", auth.signup_view, name="signup"),
    path("accounts/logout/", auth.logout_view, name="logout"),
    path("sets/<int:id>/", public.flashcard_set_detail, name="flashcard_set_detail"),
    path("sets/<int:id>/quiz", public.flashcard_set_quiz, name="quiz"),
    path("categories/<int:id>/", public.category_detail, name="category_detail"),
    path("users/<str:username>/", public.user_profile_view, name="user_profile"),
    path("settings/", user.user_settings_view, name="user_settings"),
    path("search/", public.search_view, name="search"),
    path("sets/<int:id>/edit", set.edit_set, name="edit_set"),
    path("sets/<int:id>/settings", set.set_settings, name="set_settings"),
    path("sets/<int:id>/add", set.set_add_card, name="set_add_card"),
    path("sets/new", set.set_create_new, name="set_create"),
    path("sets/<int:set_id>/edit/<int:card_id>", set.edit_flashcard_set_flashcard, name="edit_flashcard")
]
