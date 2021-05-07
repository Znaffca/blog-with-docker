from faker import Faker
import os, random


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_platform.settings")


import django

django.setup()
from django.contrib.auth.models import User
from blog_app.models import Post, Comment


def fake_init():
    """
    initializes faker object for further usage in next functions
    """
    return Faker()


def create_tag_list(faker_obj, num=10):
    """
    create a list of tags which will be constant for all posts to use
    """
    fake = faker_obj
    return fake.words(nb=num)


def create_comment_list(faker_obj, post_obj, num=5):
    """
    function creates a list of comment for post object passed to it
    :param: faker_obj
    :param: post_obj
    :param: num
    """
    for i in range(num):
        obj_prof = faker_obj.simple_profile()
        obj_txt = faker_obj.sentence(nb_words=random.randint(5, 12))
        Comment.objects.create(
            post=post_obj,
            name=obj_prof["username"],
            email=obj_prof["mail"],
            body=obj_txt,
        )


def profile_create(faker_obj=fake_init()):
    """
    function creates a fake profile for testing pruposes using a provided faker object
    """
    profile = faker_obj.simple_profile()
    user = User.objects.create(
        username=profile["username"],
        email=profile["mail"],
        password=profile["username"][::-1],
    )
    return user.id


def post_create(faker_obj, profile_obj, tag_list, num=3):
    """
    Creating a post object and comments related for each new created posts
    """
    for i in range(num):
        obj = faker_obj
        title = obj.sentence(nb_words=random.randint(5, 10))
        author = User.objects.get(id=profile_obj)
        body = " ".join(obj.paragraphs(nb=random.randint(8, 20)))
        status = "published"
        post = Post.objects.create(title=title, author=author, body=body, status=status)
        post.tags.add(", ".join(random.sample(tag_list, 1)))
        print(
            "Created post title:'{}' for user '{}'".format(post.title, author.username)
        )
        create_comment_list(obj, post)


if __name__ == "__main__":
    tags = create_tag_list(Faker(), 6)
    for i in range(6):
        fake = fake_init()
        prof = profile_create(fake)
        post_create(fake, prof, tags)
