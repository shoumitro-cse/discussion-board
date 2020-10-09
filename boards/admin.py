# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import site

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name","description")
    class Meta:
        ordering = ("-id", )