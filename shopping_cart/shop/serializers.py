"""
DRF Serializers for Shop Models.
"""
from rest_framework import serializers
from decimal import Decimal
from .models import Book, MusicAlbum, SoftwareLicense, Cart, CartItem


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book products."""
    
    weight = serializers.DecimalField(
        max_digits=6,
        decimal_places=3,
        min_value=Decimal('0.001')
    )
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'number_of_pages',
            'price', 'weight', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MusicAlbumSerializer(serializers.ModelSerializer):
    """Serializer for MusicAlbum products."""
    
    weight = serializers.DecimalField(
        max_digits=6,
        decimal_places=3,
        min_value=Decimal('0.001')
    )
    
    class Meta:
        model = MusicAlbum
        fields = [
            'id', 'artist', 'title', 'number_of_tracks',
            'price', 'weight', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SoftwareLicenseSerializer(serializers.ModelSerializer):
    """Serializer for SoftwareLicense products."""
    
    class Meta:
        model = SoftwareLicense
        fields = [
            'id', 'name', 'price', 'license_key',
            'valid_until', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem with product details."""
    
    product_type = serializers.SerializerMethodField()
    product_details = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        source='get_subtotal'
    )
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product_type', 'product_details',
            'quantity', 'subtotal', 'added_at', 'updated_at'
        ]
        read_only_fields = ['id', 'added_at', 'updated_at']
    
    def get_product_type(self, obj):
        """Return the type of product (book, music_album, software_license)."""
        return obj.content_type.model
    
    def get_product_details(self, obj):
        """Return serialized product data."""
        product = obj.product
        if not product:
            return None
            
        if isinstance(product, Book):
            return BookSerializer(product).data
        elif isinstance(product, MusicAlbum):
            return MusicAlbumSerializer(product).data
        elif isinstance(product, SoftwareLicense):
            return SoftwareLicenseSerializer(product).data
        return None


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart with calculated totals."""
    
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        source='get_total_price'
    )
    total_weight = serializers.DecimalField(
        max_digits=10,
        decimal_places=3,
        read_only=True,
        source='get_total_weight'
    )
    items_count = serializers.IntegerField(
        read_only=True,
        source='get_items_count'
    )
    
    class Meta:
        model = Cart
        fields = [
            'id', 'is_active', 'items', 'total_price',
            'total_weight', 'items_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart."""
    
    product_type = serializers.ChoiceField(
        choices=['book', 'music_album', 'software_license']
    )
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating cart item quantity."""
    
    quantity = serializers.IntegerField(min_value=0)


class ProductSequenceAnalysisSerializer(serializers.Serializer):
    """Serializer for product sequence analysis results."""
    
    product_id = serializers.UUIDField()
    most_common_next_product = serializers.UUIDField(allow_null=True)
    occurrence_count = serializers.IntegerField()


class RecommendationSerializer(serializers.Serializer):
    """Serializer for product recommendations."""
    
    product_id = serializers.UUIDField()
    frequency = serializers.IntegerField()
