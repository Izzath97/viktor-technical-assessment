"""
Shopping Cart Django Application Configuration.
"""
from django.apps import AppConfig


class ShopConfig(AppConfig):
    """Configuration for the shop application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
