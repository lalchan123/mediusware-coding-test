from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "Mediusware Company Limited"
admin.site.site_title = "Mediusware"
admin.site.index_title = "Mediusware Limited"


class variantAdmin(admin.ModelAdmin):
    list_display=['title','description','active']
    list_display_links=('title','description')
    list_filter=('title',)
    search_fields=('title','description')
    
   
class productAdmin(admin.ModelAdmin):
    list_display=('title','sku','description')
    search_fields=['title','description']
    prepopulated_fields={'sku':('title',)}

class ProductVariantAdmin(admin.ModelAdmin):
    list_display=['variant_title','variant','product']
    list_display_links=('variant_title','product')
    search_fields=('variant_title','variant','product')

class ProductVariantPriceAdmin(admin.ModelAdmin):
    list_display=['product_variant_one','product_variant_two','product_variant_three','price','stock','product']
    list_display_links=('product_variant_one','price','product')
    search_fields=('product_variant_one','price','product')



admin.site.register(Variant, variantAdmin)
admin.site.register(Product, productAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductVariantPrice, ProductVariantPriceAdmin)    