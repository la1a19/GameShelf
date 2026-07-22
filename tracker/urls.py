from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.tracker, name="tracker"),
    path("search-ajax/", views.search_games_ajax, name="search_games_ajax"),
    path("update-status/<int:item_id>/", views.update_status, name="update_status"),
    path("add-game/", views.add_game, name="add_game"),
    path("delete-game/<int:item_id>/", views.delete_game, name="delete_game"),
    path("get-notes/<int:item_id>/", views.get_notes, name="get_notes"),
    path("save-notes/<int:item_id>/", views.save_notes, name="save_notes"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]