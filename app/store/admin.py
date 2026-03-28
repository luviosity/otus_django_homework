from django.contrib import admin
from django.db.models import F

from store.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "product_list"]
    search_fields = ["name", "description"]
    search_help_text = "Enter part of name or description to search"

    def product_list(self, obj):
        return ", ".join(p.name for p in obj.products.all())


@admin.action(description="Mark as active")
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Mark as inactive")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Apply 10%% discount")
def apply_discount(modeladmin, request, queryset):
    queryset.update(price=F("price") * 0.9)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "is_active", "created_at"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]
    actions = [make_active, make_inactive, apply_discount]
    search_help_text = "Enter part of name or description to search"

    readonly_fields = ["created_at"]
    fieldsets = (
        ('Main', {
            'fields': ('name', 'category', 'price',)
        }),
        ('Tech', {
            'fields': ('is_active', 'created_at',),
            'classes': ('collapse',)
        }),
    )
