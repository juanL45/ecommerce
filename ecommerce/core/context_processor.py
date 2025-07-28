from core.models import Product,Category,Vendor,CartOrder,CartOrderProducts,ProductImages, wishlist_model,ProductReview,Address  #Wishlist
from django.db.models import Min,Max,Count
from django.contrib import messages
def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min('price'),Max('price'))
    try:
        wishlist = wishlist_model.objects.filter(user=request.user)
    except:
        messages.warning(request,"You need lo login to access wishlist")
        wishlist =None
    try:
        address = Address.objects.get(user=request.user) # antes era get
    except:
        address = None
    return {
        "categories":categories,
        "wishlist":wishlist,
        "address":address,
        "vendors":vendors,
        "min_max_price":min_max_price
    }