from django.urls import path, include
from homepage.views import *
from bookcommunity.views import *

app_name = 'bookcommunity'

urlpatterns = [
    path('', show_community, name='show_community'),
    path('create-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('get_forums_and_discussions/', get_forums_and_discussions, name='get_forums_and_discussions'),
    path('create-discussion-ajax', add_discussion_ajax, name='add_discussion_ajax'),
    path('delete_forum/<int:forum_id>/', delete_forum_ajax, name='delete_forum_ajax'),

    
]
