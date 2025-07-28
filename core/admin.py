from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from core.models import Product,Category,Vendor,CartOrder,CartOrderProducts, ProductImages, wishlist_model,ProductReview,Address,Coupon,Blog


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','title','product_image','price','featured','product_status','category','vendor','pid']
class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['title','category_image']
class VendorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['title','vendor_image']
class CartOrderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_editable =['paid_status','product_status']
    list_display = ['user','price','paid_status','order_date','product_status']
class CartOrderProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['order','invoice_no','item','image','qty','price','total']
class ProductReviewAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['user','product','review','rating']
class WishListAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['user','product','date']
class AddressAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_editable =['address','status']
    list_display = ['user','address','status']

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderProducts,CartOrderProductAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(wishlist_model,WishListAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Coupon)
admin.site.register(Blog)