from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpRequest
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from django.core.mail import send_mail

from core.models import Post
from core.forms import EmailPostForm

class PostListView(ListView):
    """Something here """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = "core/post/list.html"


def list_post(request: HttpRequest):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, "core/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, year: int, month: int, day: int, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED,
    )
    return render(request, "core/post/detail.html", {"post": post})



def post_share(request: HttpRequest, post_id: int):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        print("POST data", request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )

            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )

            send_mail(subject, message, 'compass.app.info@gmail.com', [cd['to']])

            sent = True

    else:
        form = EmailPostForm()
    return render(
            request,
            'core/post/share.html',
            {
                'post': post,
                'form': form,
                'sent': sent
            }
        )
        