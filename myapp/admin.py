from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'order_type', 'order_date', 'total_items')

    def get_fields(self, request, obj=None):
        if obj:
            return ['books', ('member', 'order_type', 'order_date')]
        return super().get_fields(request, obj)


admin.site.register(Order, OrderAdmin)

admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(Member)
admin.site.register(Review)
