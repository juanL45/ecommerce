#Dependencias
import calendar
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,get_list_or_404,redirect
from django.db.models import Count,Avg
from taggit.models import Tag
from core.models import Product,Category,Vendor,CartOrder,CartOrderProducts,ProductImages, wishlist_model,ProductReview,Address,Coupon,Blog
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from userauths.models import Profile,ContactUs
from django.core import serializers
from django.db.models.functions import ExtractMonth
import stripe
#Funciones
def index(request):
    product = Product.objects.filter(product_status="published",featured=True)
    category = Category.objects.all()
    context ={
        "products": product,
        "categories":category
    }
    return render(request,'core/index.html',context)
def product_list_view(request):
    product = Product.objects.filter(product_status="published",featured=True)
    context ={
        "products": product
    }
    return render(request,'core/product-list.html',context)
def category_list_view(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request,"core/category-list.html",context)
def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published",category=category)
    context = {
        "category":category,
        "products":products
    }
    return render(request,"core/category-product-list.html",context)
def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors":vendors
    }
    return render(request,"core/vendor-list.html",context)
def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor,product_status="published")
    context = {
        "vendor":vendor,
        "products":products
    }
    return render(request,"core/vendor-detail.html",context)
def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user,product=product).count()
        if user_review_count > 0:
            make_review=False
    
    p_image = product.p_images.all()
    context = {
        "p": product,
        "p_image":p_image,
        "make_review":make_review,
        "review_form":review_form,
        "average_rating":average_rating,
        "reviews":reviews,
        "products":products
    }
    return render(request,"core/product-detail.html",context)
def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None
    if(tag_slug):
        tag = get_list_or_404(Tag,slug=tag_slug)
        products =products.filter(tags__in=[tag])
    context = {
        "products":products,
        "tag":tag
    }
    return render(request,"core/tag.html",context)  
def ajax_add_review(request,pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating']
    )
    context = {
        'user':user.username,
        'review' :request.POST['review'],
        'rating':request.POST['rating']
    }
    average_reviews = ProductReview.objects.filter(product=product).aggregate(ratinf= Avg("rating"))
    return JsonResponse(
        {
        'bool':True,
        'context':context,
        'average_reviews':average_reviews

        }
        )
def search_view(request):
    query = request.GET.get("q")
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context = {
        "products":products,
        "query":query
    }
    return render(request,"core/search.html",context)  
def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by('-id').distinct()
    products = products.filter(price__gte = min_price)
    products = products.filter(price__lte = max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
    context = {
        'products':products
    }
    data = render_to_string("core/async/product-list.html",{'products':products})
    return JsonResponse({"data":data})
def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data= request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])])['qty']
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_session'])})
def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request,'core/cart.html',{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request,"Your cart is empty")
        return redirect("core:index")
        #return render(request,'core/cart.html',{"cart_data":'','totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.sesssion['cart_data_obj'][product_id]
            request.session['cart_data_obj']=cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty']= product_qty
            request.session['cart_data_obj']=cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})
def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        
        request.session['full_name']= full_name
        request.session['email']= email
        request.session['mobile']= mobile
        request.session['address']= address
        request.session['city']= city
        request.session['state']= state
        request.session['country']= country

        if 'cart_data_obj' in request.session:
            for p_id,item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])
            
            if request.user_is_authenticated:
                user = request.user
            else:
                user = None
            order = CartOrder.objects.create(
                user=user,
                price=total_amount,
                full_name = full_name,
                email=email,
                phone=mobile,
                adress= address,
                city=city,
                state=state,
                country=country
            )
            del request.session['full_name']
            del request.session['email']
            del request.session['mobile']
            del request.session['address']
            del request.session['city']
            del request.session['state']
            del request.session['country']
            for p_id,item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])
                cart_order_products = CartOrderProducts.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-"+str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total = float(item['qty'])*float(item['price'])
                )
        return redirect("core:checkout",order.oid)
    return redirect("core:checkout",order.oid)
def checkout(request,oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderProducts.objects.filter(order=order)
    messages.warning(request,"Coupon already activated")
    if request.method =='POST':
        code = request.POST.get('code')
        coupon = Coupon.objects.filter(code=code,active=True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request,"Coupon already activated")
                return redirect("core:checkout",order.oid)
            else:
                discount = (order.price * coupon*discount)/100
                order.coupons.add(coupon)
                order.price = discount
                order.saved += discount
                order.save()
                messages.success(request,"Coupon activated")
                return redirect("core:checkout",order.oid)
        else:
            messages.error(request,"Coupon does not exist")
            return redirect("core:checkout",order.oid)

    context = {
        "order":order,
        "order_items":order_items,
        "stripe_published_key":settings.STRIPE_PUBLIC_KEY,
    }
    return render(request,"core/checkout.html",context)
@csrf_exempt
def create_checkout_session(request,oid):
    order = CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = order.email,
        payment_method_types =['cards'],
        line_items = [
            {
            'price_data':
                    {
                        'currency':'USD',
                        'product_data':
                        {
                            'name':order.full_name,
                        },
                        'unit_amount':int(order.price*1000),
                    },
            'quantity':1
            }],
        mode='payment',
        success_url=request.build_absolute_url(reverse("core:payment-completed",args= [order.oid])) +"?session_id = {CHEKCOIT_SESSION_ID}",
        cancel_url=request.build_absolute_url(reverse("core:payment-failed"))       
       )
    order.paid_status=False
    order.stripe_payment_intent = checkout_session['id']
    order.save()
    return JsonResponse({"session_id":checkout_session.id})
@login_required
def payment_completed_view(request,oid):
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status ==False:
        order.paid_status = True
        order.save()
    context = {
        "order":order
    }
    
    return render(request,'core/payment-completed.html',context)
@login_required
def payment_failed_view(request):
    return render(request,"core/payment-failed.html")
@login_required
def customer_dashboard(request):
    order_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    

    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count = Count("id")).values("month","count")
    #orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    month =[]
    total_orders = []
    
    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i['count'])
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user = request.user,
            adress = address,
            mobile=mobile
        )
        messages.success(request,"Adress Addes Succesfully")
        return redirect("core:dashboard")
    else:
        pass
    user_profile = Profile.objects.get(user=request.user)
    context = {
        "user_profile":user_profile,  
        "orders":orders,
        "order_list":order_list,
        "address":address,
        "month":month,
        "total_orders":total_orders
        
    }
    return render(request,"core/dashboard.html",context)
def order_detail(request,id):
    order = CartOrder.objects.get(user=request.user,id=id)
    order_items = CartOrderProducts.objects.filter(order=order)
    context = {
        "order_items":order_items
    }
    return render(request,"core/order-detail.html",context)
def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})
@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.all()
    context = {
            "w":wishlist
        }
    return render(request,"core/wishlist.html",context)
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    context = {}
    wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
    
    if(wishlist_count)>0:
        context = {
            "bool":True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
            product=product,
            user=request.user
        )
        context= {
            "bool":True
        }
    return JsonResponse(context)
def remove_wishlist(request):
    pid = request.GET['id']
    wishlist =wishlist_model.objects.filter(user=request.user)
    product = wishlist_model.objects.get(id=pid)
    product.delete()
    context = {
        "bool":True,
        "wishlist":wishlist
    }
    wishlist_json = serializers.serialize('json',wishlist)
    t = render_to_string("core/async/wishlist.html",context)
    return JsonResponse({"data":t,"w":wishlist})
def contact(request):
    return render(request,"core/contact.html")
def ajax_contact_form(request):
    full_name = request.GET['fullname']
    email = request.GET['email']
    phone = request.GET['phone']
    message = request.GET['message']
    subject = request.GET['subject']
    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message

    )
    data = { 
        "bool":True,
        "message":"Message Sent Succesfully"}
    return JsonResponse({"data":data})
def about_us(request):
    return render(request,"core/about_us.html")
def purchase_guide(request):
    return render(request,"core/purchase_guide.html")
def privacy_policy(request):
    return render(request,"core/privacy_policy.html")
def terms_of_service(request):
    return render(request,"core/terms_of_service.html")
@login_required
def blogs(request):
    blogs = Blog.objects.all()
    context ={"blogs":blogs}
    return render(request,"core/blogs.html",context)
@login_required
def blog_content(request,id):
    blog = Blog.objects.filter(id=id).first()
    context ={"blog":blog}
    return render(request,"core/blog_content.html",context)

