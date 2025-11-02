"""
Django Admin Configuration for Shop Models.
"""
from django.contrib import admin
from .models import Book, MusicAlbum, SoftwareLicense, Cart, CartItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface for Book model."""
    
    list_display = ['title', 'author', 'price', 'number_of_pages', 'weight']
    search_fields = ['title', 'author']
    list_filter = ['created_at']
    ordering = ['-created_at']


@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    """Admin interface for MusicAlbum model."""
    
    list_display = ['title', 'artist', 'price', 'number_of_tracks', 'weight']
    search_fields = ['title', 'artist']
    list_filter = ['created_at']
    ordering = ['-created_at']


@admin.register(SoftwareLicense)
class SoftwareLicenseAdmin(admin.ModelAdmin):
    """Admin interface for SoftwareLicense model."""
    
    list_display = ['name', 'price', 'license_key', 'valid_until']
    search_fields = ['name', 'license_key']
    list_filter = ['created_at', 'valid_until']
    ordering = ['-created_at']


class CartItemInline(admin.TabularInline):
    """Inline for CartItem in Cart admin."""
    
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'updated_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for Cart model."""
    
    list_display = ['id', 'is_active', 'get_items_count',
                    'get_total_price', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['-created_at']
    inlines = [CartItemInline]
    
    def get_items_count(self, obj):
        return obj.get_items_count()
    get_items_count.short_description = 'Items'
    
    def get_total_price(self, obj):
        return f"€{obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'
