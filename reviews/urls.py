from django.conf.urls import url

from .views import (
    AddReviewView,
    )

urlpatterns = [
    url(r'^add_review/(?P<id>\d+)/$', AddReviewView.as_view(), name='add'),
]
