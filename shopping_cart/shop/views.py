"""
API Views for Shopping Cart System.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Book, MusicAlbum, SoftwareLicense, Cart
from .serializers import (
    BookSerializer, MusicAlbumSerializer, SoftwareLicenseSerializer,
    CartSerializer, AddToCartSerializer, ProductSequenceAnalysisSerializer,
    RecommendationSerializer
)
from .recommendations import (
    analyze_product_sequences,
    get_product_recommendations,
    find_frequently_bought_together
)


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for Book products."""
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class MusicAlbumViewSet(viewsets.ModelViewSet):
    """ViewSet for MusicAlbum products."""
    
    queryset = MusicAlbum.objects.all()
    serializer_class = MusicAlbumSerializer
    permission_classes = [AllowAny]


class SoftwareLicenseViewSet(viewsets.ModelViewSet):
    """ViewSet for SoftwareLicense products."""
    
    queryset = SoftwareLicense.objects.all()
    serializer_class = SoftwareLicenseSerializer
    permission_classes = [AllowAny]


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Cart operations with custom actions.
    """
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """
        Add a product to the cart.
        
        POST /api/carts/{cart_id}/add_item/
        Body: {
            "product_type": "book",
            "product_id": "uuid",
            "quantity": 1
        }
        """
        cart = self.get_object()
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_type = serializer.validated_data['product_type']
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        # Get the product
        product = self._get_product(product_type, product_id)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Add to cart
        cart.add_item(product, quantity)
        
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """
        Remove a product from the cart.
        
        POST /api/carts/{cart_id}/remove_item/
        Body: {
            "product_type": "book",
            "product_id": "uuid"
        }
        """
        cart = self.get_object()
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_type = serializer.validated_data['product_type']
        product_id = serializer.validated_data['product_id']
        
        product = self._get_product(product_type, product_id)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        removed = cart.remove_item(product)
        
        if removed:
            return Response(
                CartSerializer(cart).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Item not in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def update_item(self, request, pk=None):
        """
        Update item quantity in cart.
        
        POST /api/carts/{cart_id}/update_item/
        Body: {
            "product_type": "book",
            "product_id": "uuid",
            "quantity": 3
        }
        """
        cart = self.get_object()
        add_serializer = AddToCartSerializer(data=request.data)
        
        if not add_serializer.is_valid():
            return Response(
                add_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_type = add_serializer.validated_data['product_type']
        product_id = add_serializer.validated_data['product_id']
        quantity = add_serializer.validated_data['quantity']
        
        product = self._get_product(product_type, product_id)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        cart.update_item_quantity(product, quantity)
        
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """
        Clear all items from the cart.
        
        POST /api/carts/{cart_id}/clear/
        """
        cart = self.get_object()
        cart.clear()
        
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def analyze_sequences(self, request):
        """
        Analyze product addition sequences across all carts.
        
        GET /api/carts/analyze_sequences/
        
        Returns the most common product added after each product.
        """
        carts = Cart.objects.filter(is_active=True)
        sequences = analyze_product_sequences(carts)
        
        results = []
        for product_id, (next_product_id, count) in sequences.items():
            results.append({
                'product_id': product_id,
                'most_common_next_product': next_product_id,
                'occurrence_count': count
            })
        
        serializer = ProductSequenceAnalysisSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """
        Get product recommendations based on addition patterns.
        
        GET /api/carts/recommendations/?product_id={uuid}&limit=5
        """
        product_id = request.query_params.get('product_id')
        limit = int(request.query_params.get('limit', 5))
        
        if not product_id:
            return Response(
                {'error': 'product_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        carts = Cart.objects.filter(is_active=True)
        recommendations = get_product_recommendations(
            product_id, carts, limit
        )
        
        results = [
            {'product_id': pid, 'frequency': freq}
            for pid, freq in recommendations
        ]
        
        serializer = RecommendationSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def frequently_bought_together(self, request):
        """
        Get products frequently bought together.
        
        GET /api/carts/frequently_bought_together/?min_frequency=2
        """
        min_freq = int(request.query_params.get('min_frequency', 2))
        
        carts = Cart.objects.filter(is_active=True)
        pairs = find_frequently_bought_together(carts, min_freq)
        
        results = [
            {
                'products': list(pair),
                'frequency': freq
            }
            for pair, freq in pairs
        ]
        
        return Response(results)

    def _get_product(self, product_type, product_id):
        """Helper method to get product by type and ID."""
        model_map = {
            'book': Book,
            'music_album': MusicAlbum,
            'software_license': SoftwareLicense
        }
        
        model = model_map.get(product_type)
        if not model:
            return None
        
        try:
            return model.objects.get(id=product_id)
        except model.DoesNotExist:
            return None
