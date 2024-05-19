from django.urls import include, path
from data_core import views
from rest_framework import routers


app_name = "data_core"

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename="product")
router.register(r'product_images', views.ProductImageViewSet, basename="product_image")
router.register(r'tags', views.TagViewSet, basename="tag")

urlpatterns = [
    path("", views.index, name="index"),
    path("images/<int:pk>/", views.ProductImageDetailView.as_view(), name="image_detail"),
    path("products/", views.ProductListView.as_view(), name='product_list'),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path('api/', include(router.urls)),
]