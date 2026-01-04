from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Store, StoreTheme


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'owner', 'domain', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'domain', 'owner__username']
    date_hierarchy = 'created_at'


@admin.register(StoreTheme)
class StoreThemeAdmin(admin.ModelAdmin):
    list_display = ['store', 'primary_color', 'layout_width', 'updated_at']
    list_filter = ['layout_width', 'updated_at']
    search_fields = ['store__name']
    readonly_fields = ['created_at', 'updated_at']



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'store', 'created_at']
    list_filter = ['store']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'store__name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'category', 'store', 'created_at']
    list_filter = ['available', 'created_at', 'category', 'store']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'store__name']
    date_hierarchy = 'created_at'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'store', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at', 'store']
    list_editable = ['status']
    search_fields = ['user__username', 'user__email', 'store__name']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
