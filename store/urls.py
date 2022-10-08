from django.contrib import admin
from django.urls import path
from .import views
from rating import views


urlpatterns = [
    path('',views.store,name="store"),
    path('category/<slug:category_slug>/',views.store,name="Category_products"),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name="products_details"),
    path('search/',views.search,name="search"),
    path('submit_review/<int:product_id>/',views.submit_review,name="submit_review"),
]