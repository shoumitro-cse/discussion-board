# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.contrib.auth.models import User

# class Login(User):
#     pass
from django.utils.html import mark_safe
from django.utils.text import Truncator
from markdown import markdown


class Board(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = "Board"
        verbose_name = "Board"
        verbose_name_plural = "Boards"

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)# by default related_name='topic_set'
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)  # <- here

    class Meta:
        db_table = "Topic"
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 2
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 3

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)


    def get_last_five_posts(self):
        return self.posts.order_by('-created_at')[:5]


class Post(models.Model):
    message = models.TextField(max_length=5000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    class Meta:
        db_table = "Post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
