from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from . import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from . mixins import UserIsOwnerMixin
from .forms import ArticleForm, ArticleFilterForm, CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class ArticleListView(ListView):
    model = models.Article
    context_object_name = "articles"
    template_name = "html_files/article_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category", "")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ArticleFilterForm(self.request.GET)
        return context

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = models.Article
    context_object_name = "article"
    template_name = "html_files/article_info.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.article = self.get_object()
            comment.save()
            return redirect(to='articlee:article-info', pk=comment.article.pk)
        else:
            pass


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = models.Article
    template_name = "html_files/article_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articlee:article-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        article = self.get_object()
        article.status = "Виконано"
        article.save()
        return HttpResponseRedirect(reverse_lazy("articlee:article-list"))


    def get_object(self):
        article_id = self.kwargs.get('pk')
        return get_object_or_404(models.Article, pk=article_id)


class ArticleUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Article
    form_class = ArticleForm
    template_name = "html_files/article_update_form.html"
    success_url = reverse_lazy("articlee:article-list")


class ArticleDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Article
    template_name = "html_files/article_delete_form.html"
    success_url = reverse_lazy("articlee:article-list")


class CustomLoginView(LoginView):
    template_name = "html_files/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "articlee:login"


class RegisterView(CreateView):
    template_name = "html_files/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("articlee:login"))

