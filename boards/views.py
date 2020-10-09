# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

# Create your views here.

from django.http import HttpResponse, Http404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import UpdateView, ListView
from django.utils import timezone

from boards.forms import NewTopicForm, PostForm
from boards.models import Board, Topic, Post


# @login_required
def home(request):
    boards = Board.objects.all()
    return render(request,"boards/home.html", {"boards":boards})

# @method_decorator(login_required, name='dispatch')
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


#for class base pagination
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

# # for function base pagination
# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     #Here we are using the annotate QuerySet method to generate a new “column” on the fly.
#     # for topic in topics:
#     #    print(topic.replies)
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(queryset, 5)
#
#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         # fallback to the first page
#         topics = paginator.page(1)
#     except EmptyPage:
#         # probably the user tried to add a page number
#         # in the url, so we fallback to the last page
#         topics = paginator.page(paginator.num_pages)
#
#     return render(request, 'boards/topics.html', {'board': board, 'topics': topics})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True           # <-- until here

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    # def get_context_data(self, **kwargs):
    #     self.topic.views += 1
    #     self.topic.save()
    #     kwargs['topic'] = self.topic
    #     return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'boards/topic_posts.html', {'topic': topic})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    #user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user #here
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user #here
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # <- here
    else:
        form = NewTopicForm()
        # form.fields
        # form.message.help_text
        # form.message.label
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()


            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
            # return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

# # Function-Based View
# def new_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(request, 'new_post.html', {'form': form})

# urls.py
#     url(r'^new_post/$', views.new_post, name='new_post'),


# # Class-Based View
# from django.views.generic import View
# class NewPostView(View):
#     def render(self, request):
#         return render(request, 'new_post.html', {'form': self.form})
#
#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#         return render(request, 'new_post.html', {'form': form})
#
#     def get(self, request):
#         form = PostForm()
#         return render(request, 'new_post.html', {'form': form})

# urls.py
#     url(r'^new_post/$', views.NewPostView.as_view(), name='new_post'),




# # Generic Class-Based View
# from django.views.generic import CreateView
# class NewPostView(CreateView):
#     model = Post
#     form_class = PostForm
#     success_url = reverse_lazy('post_list')
#     template_name = 'new_post.html'

# urls.py
#     url(r'^new_post/$', views.NewPostView.as_view(), name='new_post'),




# https://stackoverflow.com/questions/13678933/how-can-i-pass-kwargs-in-url-in-django
# def home(request, **kwargs):
#     model = kwargs["model"]

# class myview(TemplateView):
#     def myfunction(self,request, object_id, **kwargs):
#         model = kwargs['model']

# def home(request, model, number, people):


# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     # board_list = get_list_or_404(Board, pk=pk)
#     # try:
#     #     board = Board.objects.get(pk=pk)
#     # except Board.DoesNotExist:
#     #     raise Http404
#     # print(reverse('board_topics', kwargs={'pk': 1}))
#     return render(request, 'boards/topics.html', {'board': board})