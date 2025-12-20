from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article-list"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article-info"),
    path("<int:pk>/update/", views.ArticleUpdateView.as_view(), name="article-update"),
    path("<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="article-delete"),
    path("article-create", views.ArticleCreateView.as_view(), name="article-create"),
    path("<int:pk>/complete/", views.ArticleCompleteView.as_view(), name="article-complete"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]

app_name = "articlee"