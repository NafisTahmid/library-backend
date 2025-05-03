from django.urls import path
from base.views import wish_list_views as views
urlpatterns = [
    path('create/', views.createWishList, name="create-wish-list"),
    path('get/', views.getWishList, name="get-wish-list"),
    path('delete/<int:pk>/', views.deleteWish, name="delete-wish-list")
]