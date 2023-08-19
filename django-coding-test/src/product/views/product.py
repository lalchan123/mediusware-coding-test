from django.views import generic
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q, query

from product.models import *

from product.serializer import *

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    

def ProductListView(request):
    product = Product.objects.all().order_by("-id")
    summary_prod = Product.objects.all().count()
    product_v_price = ProductVariantPrice.objects.all()
   
    
    prod_variant =ProductVariant.objects.all()
    variant =Variant.objects.all()

    sizeItem = []
    colorItem = []
    styleItem = []

    for v in variant:
        for pv in prod_variant:
            if v.title == pv.variant.title:
                if pv.variant.title == 'Size':
                    sizeItem.append(pv.variant_title)
                if pv.variant.title == 'Color':
                    colorItem.append(pv.variant_title)
                if pv.variant.title == 'Style':
                    styleItem.append(pv.variant_title)

               

    paginator = Paginator(product, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   

    context ={
        'page_obj':page_obj,
        'summary_prod':summary_prod,
        'product_v_price':product_v_price,
        'prod_variant':prod_variant,
        'variant':variant,
        'sizeItem':set(sizeItem),  
        'colorItem':set(colorItem),  
        'styleItem':set(styleItem),  
    }
    return render(request, 'products/list.html', context)  


def SearchView(request):
    product = Product.objects.all()
    prod_variant =ProductVariant.objects.all()
    variant1 =Variant.objects.all()

    sizeItem = []
    colorItem = []
    styleItem = []

    for v in variant1:
        for pv in prod_variant:
            if v.title == pv.variant.title:
                if pv.variant.title == 'Size':
                    sizeItem.append(pv.variant_title)
                if pv.variant.title == 'Color':
                    colorItem.append(pv.variant_title)
                if pv.variant.title == 'Style':
                    styleItem.append(pv.variant_title)
    
    if request.method == 'POST':
        title=request.POST['title']
        variant=request.POST['variant']
        price_from=request.POST['price_from']
        price_to=request.POST['price_to']
        date=request.POST['date']

        queryset=ProductVariantPrice.objects.all()
        
        try:
            if title and variant and price_from and price_to and date:
                queryset=queryset.filter(
                    Q(product__title__icontains=title),
                    Q(product_variant_one__variant_title__icontains=variant)|Q(product_variant_two__variant_title__icontains=variant)|Q(product_variant_three__variant_title__icontains=variant),
                    Q(price__gte=price_from, price__lte=price_to), 
                    Q(product__created_at__icontains=date),
                )
               
                   
            elif title:
                queryset=queryset.filter(
                    Q(product__title__icontains=title),
                )
                   
            elif  price_from and price_to :
                queryset=queryset.filter(
                    Q(price__gte=price_from, price__lte=price_to), 
                )
                   
            elif date:
                queryset=queryset.filter(
                    Q(product__created_at__icontains=date),
                )
                   
            elif variant :
                queryset=queryset.filter(
                    Q(product_variant_one__variant_title__icontains=variant)|Q(product_variant_two__variant_title__icontains=variant)|Q(product_variant_three__variant_title__icontains=variant),
                )
                
                   
        except:
            pass
        

        product_item = []

        for p in product:
            for qs in queryset:
                if p.title == qs.product.title:
                    product_item.append(p.title)
                   
                    

        product_item1 = []

        for pi in set(product_item):
            product = Product.objects.filter(title=pi)
            product = list(product)
            product_item1 += product
        
        context={
            'page_obj': product_item1,
            'queryset': queryset,
            'variant':variant1,
            'sizeItem':set(sizeItem),  
            'colorItem':set(colorItem),  
            'styleItem':set(styleItem), 
        }
        return render(request, 'products/search.html', context)
    

def EditProductView(request, id):
    variants = Variant.objects.filter(active=True).values('id', 'title')
    context={
        'variants': list(variants.all()),
        'id': id,
    }    
        
    return render(request, 'products/update.html', context)    
    



@api_view(['POST'])   
def CreateProductApi(request):
    try:
        productName = request.data['productName']
        productSku = request.data['productSku']
        productDescription = request.data['productDescription']
        file_path = request.data['file_path']
        productVariant = request.data['productVariant']
        productVariantPrice = request.data['productVariantPrice']
        
        product = Product.objects.create(title=productName, sku=productSku, description=productDescription)

        ProductImage.objects.create(product=product, file_path=file_path)

        for i in productVariant:
            if i['option']==1:
                for pvl in range(len(i['tags'])):
                    variant = Variant.objects.get(title='Size')
                    ProductVariant.objects.create(variant_title=i['tags'][pvl],variant=variant,product=product)
            if i['option']==2:
                for pvl in range(len(i['tags'])):
                    variant = Variant.objects.get(title='Color')
                    ProductVariant.objects.create(variant_title=i['tags'][pvl],variant=variant,product=product)
            if i['option']==3:
                for pvl in range(len(i['tags'])):
                    variant = Variant.objects.get(title='Style')
                    ProductVariant.objects.create(variant_title=i['tags'][pvl],variant=variant,product=product)


        for pvp in productVariantPrice:
            alength = len(pvp['title'].split("/"))-1
            count = 0
            for pl in range(alength):
                if pl==0:
                    count+=1
                    product_variant_one=ProductVariant.objects.get(variant_title=pvp['title'].split("/")[pl],product=product)
                if pl==1:
                    count+=1
                    product_variant_two=ProductVariant.objects.get(variant_title=pvp['title'].split("/")[pl],product=product)
                if pl==2:
                    count+=1
                    product_variant_three=ProductVariant.objects.get(variant_title=pvp['title'].split("/")[pl],product=product)

            if count==1:
                ProductVariantPrice.objects.create(
                    product_variant_one=product_variant_one,
                    price=pvp['price'],
                    stock=pvp['stock'],
                    product=product
                )
            if count==2:
                ProductVariantPrice.objects.create(
                    product_variant_one=product_variant_one,
                    product_variant_two=product_variant_two,
                    price=pvp['price'],
                    stock=pvp['stock'],
                    product=product
                )
            if count==3:
                ProductVariantPrice.objects.create(
                    product_variant_one=product_variant_one,
                    product_variant_two=product_variant_two,
                    product_variant_three=product_variant_three,
                    price=pvp['price'],
                    stock=pvp['stock'],
                    product=product
                )


        return Response({
            'status': status.HTTP_200_OK, 
            'message':"Product Created Successfully", 
        })
           
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Something error!"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])   
def GetProductUpdateApi(request, id):
    try:
        product = Product.objects.get(id=id)
        productImage = ProductImage.objects.filter(product=product)
        productVariant = ProductVariant.objects.filter(product=product)
        productVariantPrice = ProductVariantPrice.objects.filter(product=product)
        productserializer = ProductSerializers(product, many=False)       
        product_image_serializer = ProductImageSerializers(productImage, many=True)  
        product_variant_serializer = ProductVariantSerializers(productVariant, many=True)  
        product_variant_price_serializer = ProductVariantPriceSerializers(productVariantPrice, many=True) 

        return Response({
            'status': status.HTTP_200_OK, 
            'product': productserializer.data,
            'productImage': product_image_serializer.data,
            'productVariant': product_variant_serializer.data,
            'productVariantPrice': product_variant_price_serializer.data,
        })
           
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Something error!"}, status=status.HTTP_400_BAD_REQUEST)    
        

@api_view(['PUT'])   
def ProductUpdateApi(request, id):
    try:
        productName = request.data['productName']
        productSku = request.data['productSku']
        productDescription = request.data['productDescription']
        file_path = request.data['file_path']
        productVariant = request.data['productVariant']
        productVariantPrice = request.data['productVariantPrice']
        
        product = Product.objects.get(id=id)
        product.title=productName
        product.sku=productSku
        product.description=productDescription
        product.save()


        product_image = ProductImage.objects.filter(product=product)
        
        if not product_image.count()==0:
            product_image1 = ProductImage.objects.get(product=product)
            product_image1.file_path=file_path
            product_image1.save()
        else:
            if file_path: 
                ProductImage.objects.create(product=product, file_path=file_path)   
       

    
        for pvp in productVariantPrice:
            alength = len(pvp['title'].split("/"))-1
            count = 0
            for pl in range(alength):
                if pl==0:
                    count+=1
                    product_variant_one=ProductVariant.objects.get(variant_title=pvp['title'].split("/")[pl],product=product)
                if pl==1:
                    count+=1
                    product_variant_two=ProductVariant.objects.get(variant_title=pvp['title'].split("/")[pl],product=product)
                if pl==2:
                    count+=1
                    product_variant_three=ProductVariant.objects.get(variant_title=pvp['title'].split("/")[pl],product=product)
            if count==1:
                product_variant_price = ProductVariantPrice.objects.get(product=product, product_variant_one=product_variant_one)
                product_variant_price.price = pvp['price']
                product_variant_price.stock = pvp['stock']
                product_variant_price.save()
                
            if count==2:
                product_variant_price = ProductVariantPrice.objects.get(product=product, product_variant_one=product_variant_one, product_variant_two=product_variant_two)
                product_variant_price.price = pvp['price']
                product_variant_price.stock = pvp['stock']
                product_variant_price.save()
            if count==3:
                product_variant_price = ProductVariantPrice.objects.get(product=product, product_variant_one=product_variant_one, product_variant_two=product_variant_two, product_variant_three=product_variant_three)
                product_variant_price.price = pvp['price']
                product_variant_price.stock = pvp['stock']
                product_variant_price.save()

        return Response({
            'status': status.HTTP_200_OK, 
            'message':"Product Updated Successfully", 
        })
           
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Something error!"}, status=status.HTTP_400_BAD_REQUEST) 
