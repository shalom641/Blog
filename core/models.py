from django.db import models
from django.contrib.auth.models import User

# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["timestamp", ]


# Post Model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # Author
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Image
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)  # Likes

    def __str__(self):
        return self.title[:50]

    def total_likes(self):
        return self.likes.count()

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"


# Intermediary model to prevent multiple likes
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensures that a user can only like a post once

    def __str__(self):
        return f"{self.user} liked {self.post.title}"
