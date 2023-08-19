from rest_framework import serializers
from product.models import *


class VariantSerializers(serializers.ModelSerializer):
    class Meta:
        model= Variant
        fields= ['id', 'title']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields= '__all__'

class ProductImageSerializers1(serializers.ModelSerializer):
    class Meta:
        model= ProductImage
        fields= '__all__'    
 

class ProductImageSerializers(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model= ProductImage
        fields= ['id', 'product', 'file_path']    


class ProductVariantSerializers1(serializers.ModelSerializer):
    class Meta:
        model= ProductVariant
        fields= '__all__'  

class ProductVariantSerializers(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model= ProductVariant
        fields= ['id', 'product', 'variant_title','variant']  
              
class ProductVariantPriceSerializers1(serializers.ModelSerializer):
    class Meta:
        model= ProductVariantPrice
        fields= '__all__'    

class ProductVariantPriceSerializers(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.title')
    product_variant_one = serializers.ReadOnlyField(source='product_variant_one.variant_title')
    product_variant_two = serializers.ReadOnlyField(source='product_variant_two.variant_title')
    product_variant_three = serializers.ReadOnlyField(source='product_variant_three.variant_title')
    class Meta:
        model= ProductVariantPrice
        fields= ['id', 'product', 'price','stock','product_variant_one','product_variant_two','product_variant_three']

