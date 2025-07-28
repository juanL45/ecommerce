from django import views
from django.urls import path,include
from core.views import category_list_view,index,product_list_view,category_product_list_view,vendor_list_view,vendor_detail_view,product_detail_view,tag_list,ajax_add_review,search_view,filter_product,add_to_cart,cart_view,delete_item_from_cart,update_cart,checkout,payment_completed_view,payment_failed_view,customer_dashboard,order_detail,make_address_default,wishlist_view,add_to_wishlist,remove_wishlist, contact,about_us,purchase_guide,privacy_policy,terms_of_service,ajax_contact_form,blogs
from core import views
app_name = "core"

urlpatterns = [
    path("",index,name="index"),
    path("products/",product_list_view,name="product-list"),
    path("product/<pid>/",product_detail_view,name="product-detail"),
    path("category/",category_list_view,name="category-list"),
    path("category/<cid>/",category_product_list_view,name="category-product-list"),
    path("vendors/",vendor_list_view,name="vendor-list"),
    path("vendors/<vid>/",vendor_detail_view,name="vendor-detail"),
    path("product/tag/<slug:tag_slug>/",tag_list,name="tags"),
    path("ajax-add-review/<pid>",ajax_add_review,name="ajax-add-review"),
    path("search/",search_view,name="search"),
    path("filter-products/",filter_product,name="filter_product"),
    path("add-to-cart/",add_to_cart,name="add_to_cart"),
    path("cart/",cart_view,name="cart"),
    path("delete-from-cart/",delete_item_from_cart,name="delete-from-cart"),
    path("update-cart/",update_cart,name="update-cart"),
    path("checkout/<oid>",checkout,name="checkout"),
    path("paypal/",include('paypal.standard.ipn.urls')),
    path("payment-completed/<oid>/",payment_completed_view,name="payment-completed"),
    path("payment-failed/",payment_failed_view,name="payment-failed"),
    path("dashboard/",customer_dashboard,name="dashboard"),
    path("dashboard/order/<int:id>",order_detail,name="order-detail"),
    path("make_default_address",make_address_default,name="make_default_address"),
    path("wishlist",wishlist_view,name="wishlist"),
    path("add-to-wishlist",add_to_wishlist,name="add-to-wishlist"),
    path("remoce-from-wishlist",remove_wishlist,name="remoce-from-wishlist"),

    #Otras
    path("contact/",contact,name="contact"),
    path("ajax-contact-form/",ajax_contact_form,name="ajax-contact-form"),
    path("about_us/",about_us,name="about_us"),
    path("purchase_guide/",purchase_guide,name="purchase_guide"),
    path("privacy_policy/",privacy_policy,name="privacy_policy"),
    path("terms_of_service/",terms_of_service,name="terms_of_service"),
    path("save_checkout_info/",views.save_checkout_info,name="save_checkout_info"),
    path("api/cerate_checkout_session/<oid>",views.create_checkout_session,name="cerate_checkout_session"),
    path("blogs/",blogs,name="blogs"),
    path("blog_content/<id>",views.blog_content,name="blog_content"),



    
]