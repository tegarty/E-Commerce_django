from django.conf.urls import url

from .views import (
    AddReviewView,
    UpdateReviewView,
    DeleteReviewView,
    )

urlpatterns = [
    url(r'^add_review/(?P<id>\d+)/$', AddReviewView.as_view(), name='add'),
    url(r'^update_review/(?P<id>\d+)/$', UpdateReviewView.as_view(), name='update'),
    url(r'^delete_review/(?P<id>\d+)/$', DeleteReviewView.as_view(), name='delete'),
]
