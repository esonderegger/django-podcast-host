from django.urls import include, path
from podcasts import views

urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('api/<pod_slug>/items/<slug>', views.ItemDetail.as_view(), name="item"),
    path('api/<slug>/items', views.ItemList.as_view(), name="items"),
    path('api/<pod_slug>/categories/<slug>', views.CategoryDetail.as_view(), name="category"),
    path('api/<slug>/categories', views.CategoryList.as_view(), name="categories"),
    path('api/<slug>', views.PodcastDetail.as_view(), name="podcast"),
    path('api/', views.PodcastList.as_view(), name="podcasts"),
    path('<slug>/feed.xml', views.xmlfeed, name="feed"),
    path('<slug>/<item_slug>', views.itempage, name="item"),
    path('<slug>', views.htmlpage, name="feed"),
    path('', views.listpage, name="podcasts"),
]
