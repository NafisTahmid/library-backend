from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Order, OrderItem, ShippingAddress, Review
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']
    
    def get_isAdmin(self, obj):
        return obj.is_staff

    def get__id(self, obj):
        return obj.id

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
        
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    isAdmin = serializers.BooleanField(required=False, default=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password', 'isAdmin']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        is_admin = validated_data.pop('isAdmin', False)
        
        user = User.objects.create(
            **validated_data,
            is_staff=is_admin
        )
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        # Convert the created user to the same format as UserSerializer
        return UserSerializer(instance).data

class UserSerializerWithToken(UserSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
    
    def get__id(self, obj):
        return obj.id
    
    def get_isAdmin(self, obj):
        return obj.is_staff
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
class BookSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Book
        fields = ['_id', 'name', 'image', 'author', 'genre', 'description', 'rating', 'numReviews', 'price','countInStock', 'createdAt', 'user', 'reviews']
    
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Order
        fields = '__all__'
    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data
    
    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False)
            return address.data
        except:
            address = False
        return address
    
    def get_user(self, obj):
        serializer = UserSerializer(obj.user, many=False)
        return serializer.data
