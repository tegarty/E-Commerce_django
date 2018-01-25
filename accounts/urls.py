from django.conf.urls import url
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    )

from .views import (
    RegisterView,
    activate_user_view,
    UserLoginView,
    UserLogoutView,
    UserChangePasswordView,
    UserProfileView,
    ProfileUpdateView,
    ProfileDeleteView,
    )

urlpatterns = [
    url(r'^activate/(?P<code>[a-zA-Z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^register/', RegisterView.as_view(), name='register'),


    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='logout'),

    url(r'^change_password/$', UserChangePasswordView.as_view(), name='change_password'),

    url(r'^profile/$', UserProfileView.as_view(), name='profile'),
    url(r'^profile/update/(?P<pk>\d+)/$', ProfileUpdateView.as_view(), name='update'),



    url(r'^profile/delete/$', ProfileDeleteView.as_view(), name='delete'),

    # url(r'^profile/update/$', ProfileUpdateView.as_view(), name='update'),

    # url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),

    url(r'^reset_password/$', password_reset, {
        'template_name': 'accounts/reset_password.html',
        'post_reset_redirect': 'accounts:password_reset_done',
        'email_template_name': 'accounts/reset_password_email.html',
        }, name='password_reset'),

    url(r'^reset_password/done/$', password_reset_done,
        {'template_name': 'accounts/reset_password_done.html'}, name='password_reset_done'),

    url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {'post_reset_redirect': 'accounts:password_reset_complete',
         'template_name': 'accounts/reset_password_confirm.html',
         }, name='password_reset_confirm'),

    url(r'^reset_password/complete/$', password_reset_complete,
        {'template_name': 'accounts/reset_password_complete.html'}, name='password_reset_complete'),
]
