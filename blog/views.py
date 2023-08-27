from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from blog.models import Post
from .forms import EmailPostForm


# def post_list(request):
#     post_lists = Post.published.all()
#     # Постраничная разбивка с 3 постами на страницу
#     paginator = Paginator(post_lists, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, day, month, year, body):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=body,
                             publish__day=day,
                             publish__month=month,
                             publish__year=year)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


class PostListView(ListView):
    """Альтернативное представление списка постов"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    """Извлечь пост по индетификатору id. Поделиться постом с другом"""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST': # POST –  форма передается на обработку.
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # данные валидируются методом is_valid() формы. Указанный метод проверяет допустимость введенных
            #  в форму данных и возвращает значение True, если все поля содержат валидные данные. Если какое-либо
            #   поле содержит не валидные данные, то is_valid() возвращает значение False. Список ошибок валидации
            #    можно получить посредством form.errors.
            cd = form.cleaned_data
            # ... отправить электронное письмо
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s ({cd['email']}) comments: {cd['comments']}"
            send_mail(subject, message, 'novozhilov812@gmail.com',
                      [cd['to']])
            sent = True

    else: #     Запрос GET, пользователю должна быть отображена пустая форма,
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})
