"""
Product and Shopping Cart Models.

This module implements a clean, extensible product hierarchy and shopping cart
system following SOLID principles and Django best practices.
"""
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid


class Product(models.Model):
    """
    Abstract base class for all products.
    Implements common product attributes and behavior.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def get_weight(self):
        """Return weight in kilograms. Override in subclasses if applicable."""
        return Decimal('0.00')

    def __str__(self):
        return f"{self.__class__.__name__} - {self.id}"


class Book(Product):
    """
    Book product with physical properties.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    number_of_pages = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        help_text="Weight in kilograms"
    )

    class Meta:
        db_table = 'books'
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['title']),
        ]

    def get_weight(self):
        return self.weight

    def __str__(self):
        return f"{self.title} by {self.author}"


class MusicAlbum(Product):
    """
    Music album (CD) product with physical properties.
    """
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    number_of_tracks = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        help_text="Weight in kilograms"
    )

    class Meta:
        db_table = 'music_albums'
        indexes = [
            models.Index(fields=['artist']),
            models.Index(fields=['title']),
        ]

    def get_weight(self):
        return self.weight

    def __str__(self):
        return f"{self.title} by {self.artist}"


class SoftwareLicense(Product):
    """
    Software license product (digital, no weight).
    """
    name = models.CharField(max_length=255)
    license_key = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    valid_until = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'software_licenses'
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_weight(self):
        return Decimal('0.00')

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Shopping cart that can contain multiple products.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']

    def add_item(self, product, quantity=1):
        """
        Add a product to the cart or update quantity if it exists.
        
        Args:
            product: Product instance (Book, MusicAlbum, or SoftwareLicense)
            quantity: Number of items to add
            
        Returns:
            CartItem: The created or updated cart item
        """
        content_type = ContentType.objects.get_for_model(product)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            content_type=content_type,
            object_id=product.id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item

    def remove_item(self, product):
        """
        Remove a product from the cart.
        
        Args:
            product: Product instance to remove
            
        Returns:
            bool: True if item was removed, False if not found
        """
        content_type = ContentType.objects.get_for_model(product)
        deleted, _ = CartItem.objects.filter(
            cart=self,
            content_type=content_type,
            object_id=product.id
        ).delete()
        return deleted > 0

    def update_item_quantity(self, product, quantity):
        """
        Update the quantity of a product in the cart.
        
        Args:
            product: Product instance
            quantity: New quantity (0 to remove)
        """
        if quantity <= 0:
            return self.remove_item(product)
        
        content_type = ContentType.objects.get_for_model(product)
        cart_item = CartItem.objects.filter(
            cart=self,
            content_type=content_type,
            object_id=product.id
        ).first()
        
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
            return cart_item
        return None

    def clear(self):
        """Remove all items from the cart."""
        self.items.all().delete()

    def get_total_price(self):
        """
        Calculate total price of all items in the cart.
        
        Returns:
            Decimal: Total price in euros
        """
        total = Decimal('0.00')
        for item in self.items.all():
            product = item.product
            if product:
                total += product.price * item.quantity
        return total

    def get_total_weight(self):
        """
        Calculate total weight of all physical items in the cart.
        
        Returns:
            Decimal: Total weight in kilograms
        """
        total = Decimal('0.00')
        for item in self.items.all():
            product = item.product
            if product:
                total += product.get_weight() * item.quantity
        return total

    def get_items_count(self):
        """Return total number of items in cart."""
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    def __str__(self):
        return f"Cart {self.id} - {self.get_items_count()} items"


class CartItem(models.Model):
    """
    Represents a product added to a cart with quantity.
    Uses generic foreign key to support all product types.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    product = GenericForeignKey('content_type', 'object_id')
    
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        ordering = ['added_at']
        indexes = [
            models.Index(fields=['cart', 'content_type', 'object_id']),
        ]
        unique_together = [['cart', 'content_type', 'object_id']]

    def get_subtotal(self):
        """Calculate subtotal for this cart item."""
        if self.product:
            return self.product.price * self.quantity
        return Decimal('0.00')

    def __str__(self):
        return f"{self.product} x{self.quantity} in cart {self.cart.id}"
