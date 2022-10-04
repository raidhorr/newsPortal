# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import PostFilter
from .forms import PostForm
from .models import Post
from .tasks import email_article


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    ordering = '-time_in'
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(LoginRequiredMixin, CreateView):
    login = '/sign/login'
    redirect_field_name = 'redirect_to'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class ArticleCreate(LoginRequiredMixin, CreateView):
    login = '/sign/login'
    redirect_field_name = 'redirect_to'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.message = 'A'
        post.save()
        pk = post.id
        email_article.delay(pk)
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.message = 'N'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    login = '/sign/login'
    redirect_field_name = 'redirect_to'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.message = 'A'
        post.save()

        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    login = '/sign/login'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

