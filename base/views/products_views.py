from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import BookSerializer
from base.models import Book, Review
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from base.products import products
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword', '')
    page = request.query_params.get('page', 1)
    
    if query:
        products = Book.objects.filter(name__icontains=query).order_by('_id')
    else:
        products = Book.objects.all().order_by('_id')
    
    paginator = Paginator(products, 6)

    try:
        page = int(page)
        products_page = paginator.page(page)
    except (PageNotAnInteger, ValueError):
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    serializer = BookSerializer(products_page, many=True)
    
    return Response({
        "products": serializer.data,
        "page": products_page.number,
        "pages": paginator.num_pages
    })

@api_view(['GET'])
def getProduct(request, pk):
   product = Book.objects.get(pk=pk)
   serializer = BookSerializer(product, many=False)
   return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request,pk):
    selectedProduct = Book.objects.get(pk=pk)
    selectedProduct.delete()
    return Response("Product deleted successfully :D")


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user =request.user
    product = Book.objects.create(
        user = request.user,
        name = 'Sample name',
        price = 0,
        author = 'Sample author',
        countInStock = 0,
        genre = 'Sample genre',
        description = 'Sample description' 

    )
    serializer = BookSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    product = Book.objects.get(_id=pk)
    data = request.data
    product.name = data['name']
    product.price = data['price']
    product.author = data.get('author', product.author)
    product.countInStock = data['countInStock']
    product.genre = data.get('genre', product.author)
    product.description = data['description']

    product.save()
    serializer = BookSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def uploadImage(request):
    data = request.data
    product_id = data['product_id']
    product = Book.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded successfully :D')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    product = Book.objects.get(_id=pk)
    user = request.user
    data = request.data

    # 1. Review already exists
    already_exists = product.review_set.filter(user=user).exists()
    if already_exists:
        content = {'detail': 'Review already exists'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. No rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating here'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3. Create new review
    else:
        review = Review.objects.create(
            book = product,
            user = user,
            name = user.first_name,
            rating = data['rating'],
            comment = data['comment']

        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total / len(reviews)
        product.save()
        return Response('Review added')
    
"""Get top products"""
@api_view(["GET"])
def getTopBooks(request):
    topProducts = Book.objects.filter(rating__gte=4).order_by("-rating")[0:5]
    serializer = BookSerializer(topProducts, many=True)
    return Response(serializer.data)