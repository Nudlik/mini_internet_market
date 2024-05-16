from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory_count', 'child_category']

    @admin.display(description='Кол-во подкатегории')
    def subcategory_count(self, obj):
        return Category.objects.filter(child_category=obj).count()
