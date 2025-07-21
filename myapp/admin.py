from django.contrib import admin
from myapp.models import Product,Cart,Buy,Book_rent,Review,Category
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Buy)
admin.site.register(Book_rent)
admin.site.register(Review)
admin.site.register(Category)