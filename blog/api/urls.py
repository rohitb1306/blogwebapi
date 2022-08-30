from django.urls import path,include
from blog.api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('blogcrud',views.BlogViewSets,basename="Blog")
router.register('comments',views.CommentViewSets,basename="comment")

urlpatterns=[
    path('',include(router.urls))
]