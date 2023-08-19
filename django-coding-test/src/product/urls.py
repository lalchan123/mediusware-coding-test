from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView, ProductListView, SearchView, EditProductView, CreateProductApi, GetProductUpdateApi, ProductUpdateApi
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    # path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
    #     'product': True
    # }), name='list.product'),
    path('list/', ProductListView, name='list.product'),
    path('search/', SearchView, name='search'),
    path('edit/<int:id>/', EditProductView, name='edit'),

    path('createproduct-api/', CreateProductApi, name='product.createproduct'),
    path('getproductupdate-api/<int:id>/', GetProductUpdateApi, name='product.getproductupdate'),
    path('productupdate-api/<int:id>/', ProductUpdateApi, name='product.productupdate'),
]
