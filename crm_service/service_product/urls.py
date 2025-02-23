from django.urls import path

from .views import ProductListView, ProductCreateView, ProductDetailView

app_name = "service_product"
urlpatterns = [
    path("", ProductListView.as_view(), name="service_list"),
    path("new/", ProductCreateView.as_view(), name="service_create"),
    path("<int:pk>/", ProductDetailView.as_view(), name="service_detail"),
]
