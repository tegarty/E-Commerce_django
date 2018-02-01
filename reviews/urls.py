from django.conf.urls import url

from .views import (
    AddReviewView,
    DeleteReviewView,
    )

urlpatterns = [
    url(r'^add_review/(?P<id>\d+)/$', AddReviewView.as_view(), name='add'),
    url(r'^delete_review/(?P<id>\d+)/$', DeleteReviewView.as_view(), name='delete'),
]
