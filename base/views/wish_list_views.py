from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import WishListSerializer
from base.models import WishList

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createWishList(request):
    user = request.user
    data = request.data
    wishList = WishList.objects.create(
        user=request.user,
        name = data["name"],
        genre = data["genre"],
        details = data["details"]
    )
   
    serializer = WishListSerializer(wishList, many=False)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def getWishList(request):
    wishLists = WishList.objects.all()
    serializer = WishListSerializer(wishLists, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteWish(request,pk):
    selectedWish = WishList.objects.get(pk=pk)
    selectedWish.delete()
    return Response("Wishlist marked as done :D")
    