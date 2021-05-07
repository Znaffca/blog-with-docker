from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from .forms import EmailPostForm, CommentForm
from .models import Post
from taggit.models import Tag


"""
This view is currently not used/replaced by single dunction view to implement tagging filtering
"""


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"  # name defined here is passed to the template, default (if not provided) is object_list
    paginate_by = 5
    template_name = "blog_app/post/list.html"


def post_list(request, tag_slug=None):
    """
    current view function is overwritten by more generic class-based view
    """
    obj_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        obj_list = obj_list.filter(tags__in=[tag])
    paginator = Paginator(obj_list, 5)  # limit to 3 posts in the simple page
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request, "blog_app/post/list.html", {"posts": posts, "page": page, "tag": tag}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tag_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    return render(
        request,
        "blog_app/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": comment_form,
            "new_comment": new_comment,
            "similar_posts": similar_posts,
        },
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    mail_to_send = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{} recommends you to read '{}'".format(data["name"], post.title)
            message = "Read '{}' at {}.\n\n{}'s comments: {}".format(
                post.title, post_url, data["name"], data["comments"]
            )
            send_mail(subject, message, "kontakt.gitlabs@gmail.com", [data["to"]])
            mail_to_send = True
    else:
        form = EmailPostForm()
    return render(
        request,
        "blog_app/post/share.html",
        {"post": post, "form": form, "sent": mail_to_send},
    )
