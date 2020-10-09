"""discussion_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# from django.urls import include

from boards import views as board_view, models
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #for home
    # url(r'^$', board_view.home, name='home'),
    url(r'^$', board_view.BoardListView.as_view(), name='home'),

    #for boards app
    url(r'^boards/(?P<pk>\d+)/$', board_view.TopicListView.as_view(), name='board_topics'),
    # url(r'^boards/(?P<pk>\d+)/$', board_view.board_topics, name='board_topics'),#function base pagination
    url(r'^boards/(?P<pk>\d+)/new/$', board_view.new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', board_view.PostListView.as_view(), name='topic_posts'),
    # url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', board_view.topic_posts, name='topic_posts'),#function base pagination
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', board_view.reply_topic, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        board_view.PostUpdateView.as_view(), name='edit_post'),

    #for accounts app
    url(r'^accounts/signup/$', accounts_views.signup, name='signup'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    #password reset
    url(r'^accounts/reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ),
        name='password_reset'),

    url(r'^accounts/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),

    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
        #http://127.0.0.1:8000/accounts/reset/Mw/4po-2b5f2d47c19966e294a1/

    url(r'^accounts/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

    #for password change
    url(r'^accounts/settings/password/$', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
        name='password_change'),
    url(r'^accounts/settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),

    #for my account
    url(r'^accounts/settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
]








# url(r'^$', views.home, kwargs=dict(model=models.Board, number="123", people="Male"), name='home'),
#url(r'^download/template/(?P<object_id>\d+)/$', views.myview().myfunction, kwargs=dict(model=models.userModel), name="sample")
#url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'), #def board_topics(request, pk):
#url(r'^boards/(\d+)/$', views.board_topics, name='board_topics'), # any name arg => def board_topics(request, board_id):

# url(r'^', include('user_account.urls')),


# https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html
# List of Useful URL Patterns
# The trick part is the regex. So I prepared a list of the most used URL patterns. You can always refer to this list when you need a specific URL.

# Primary Key AutoField
# Regex 	(?P<pk>\d+)
# Example 	url(r'^questions/(?P<pk>\d+)/$', views.question, name='question')
# Valid URL 	/questions/934/
# Captures 	{'pk': '934'}

# Slug Field
# Regex 	(?P<slug>[-\w]+)
# Example 	url(r'^posts/(?P<slug>[-\w]+)/$', views.post, name='post')
# Valid URL 	/posts/hello-world/
# Captures 	{'slug': 'hello-world'}

# Slug Field with Primary Key
# Regex 	(?P<slug>[-\w]+)-(?P<pk>\d+)
# Example 	url(r'^blog/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', views.blog_post, name='blog_post')
# Valid URL 	/blog/hello-world-159/
# Captures 	{'slug': 'hello-world', 'pk': '159'}

# Django User Username
# Regex 	(?P<username>[\w.@+-]+)
# Example 	url(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile')
# Valid URL 	/profile/vitorfs/
# Captures 	{'username': 'vitorfs'}

# Year
# Regex 	(?P<year>[0-9]{4})
# Example 	url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive, name='year')
# Valid URL 	/articles/2016/
# Captures 	{'year': '2016'}

# Year / Month
# Regex 	(?P<year>[0-9]{4})/(?P<month>[0-9]{2})
# Example 	url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive, name='month')
# Valid URL 	/articles/2016/01/
# Captures 	{'year': '2016', 'month': '01'}



# Flattened Index
#
# url(r'^questions/(?P<pk>\d+)/$', views.question_details, name='question_details'),
# url(r'^posts/(?P<slug>[-\w]+)/$', views.post, name='post'),
# url(r'^blog/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', views.blog_post, name='blog_post'),
# url(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_profile),
# url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
# url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
# url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail)