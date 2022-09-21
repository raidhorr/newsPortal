from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author = Author.objects.get(user_id=self.user)
        posts = Post.objects.filter(author=author).values('rating')
        rating = sum([post['rating'] for post in posts]) * 3
        comments = Comment.objects.filter(author=author).values('rating')
        rating += sum([comment['rating'] for comment in comments])
        for post in posts:
            comments_author = Comment.objects.filter(post=post['id']).values('rating')
            rating += sum([comment['rating'] for comment in comments_author])
        self.rating = rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    news = 'N'
    article = 'A'
    MESSAGE = [(news, 'новость'), (article, 'статья')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    message = models.CharField(max_length=1, choices=MESSAGE, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}: {self.text[:20]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
