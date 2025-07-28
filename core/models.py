from email.policy import default
from pyexpat import model
from unicodedata import decimal
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
#from ckeditor_uploader.fields import RichTextUploadingField
STATUS_CHOICE = (
    ("processing","En Proceso"),
    ("shipped","Enviado"),
    ("delivered","Entregado")
)

STATUS = (
    ("draft","Borrador"),
    ("disabled","Desactivado"),
    ("rejected","Rechazado"),
    ("in_review","En Revision"),
    ("published","Publicado"),
)


RATING = (
    ("1","⭐✧✧✧✧"),
    ("2","⭐⭐✧✧✧"),
    ("3","⭐⭐⭐✧✧"),
    ("4","⭐⭐⭐⭐✧"),
    ("5","⭐⭐⭐⭐⭐"),
)
def user_directory_path(instance,filename):
    return 'user{0}/{1}'.format(instance.user.id,filename)
class Category(models.Model):
    cid = ShortUUIDField(unique=True,prefix="cat",alphabet="abcdefgf12345")
    
    title = models.CharField(max_length=254,default='Categoria' )
    image = models.ImageField(upload_to="category",default='category.jpg')
    description = models.TextField(null=True,blank=True,default='Categoria')
    category_status = models.BooleanField(null=False,default=False)

    class Meta:
        verbose_name_plural="Categorias"
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    def __str__(self):
        return self.title
class Tags(models.Model):
    pass
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True,prefix="ven",alphabet="abcdefgf12345")
    
    title = models.CharField(max_length=254,default='Vendedor' )
    image = models.ImageField(upload_to=user_directory_path,default='vendor.jpg')
    cover_image = models.ImageField(upload_to=user_directory_path,default='vendor.jpg')
    description = CKEditor5Field(config_name='extends',null=True,blank=True,default='Descripcion')

    address = models.CharField(max_length=255,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    chat_resp_time = models.CharField(max_length=255,default="100")
    shipping_on_time =models.CharField(max_length=255,default="100")
    autentic_rating =models.CharField(max_length=255,default="100")
    days_return =models.CharField(max_length=255,default="100")
    warranty_period = models.CharField(max_length=255,default="100")
    user = models.ForeignKey(User,on_delete=models.RESTRICT,null=False)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        verbose_name_plural="Vendedores"
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(unique=True,prefix="prod",alphabet="abcdefgf12345")
    user = models.ForeignKey(User,on_delete=models.RESTRICT,null=False)
    category = models.ForeignKey(Category,on_delete=models.RESTRICT,null=False,related_name="category")
    vendor = models.ForeignKey(Vendor,on_delete=models.RESTRICT,null=False,default="0",related_name="product")

    title = models.CharField(max_length=254,default='Este es un Producto')
    image = models.ImageField(upload_to=user_directory_path,default='product.jpg')
    description = CKEditor5Field(config_name='extends', null=True, blank=True)
    price = models.DecimalField(max_digits= 12,decimal_places=2,default="0.00")
    old_price = models.DecimalField(max_digits= 12,decimal_places=2,default="0.00")
    specifications = CKEditor5Field(config_name='extends', null=True, blank=True)
    type = models.CharField(max_length=100,default="Type",null=True,blank=True)
    stock_count = models.CharField(max_length=100,default="0",null=True,blank=True)
    life = models.CharField(max_length=100,default="100 dias",null=True,blank=True)
    mfd = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    tags = TaggableManager(blank=True)
    #tags = models.ForeignKey(Tags,on_delete=models.RESTRICT,null=False)
    product_status = models.CharField(choices=STATUS,max_length=10,default='in_review')
    status = models.BooleanField(default=True)
    in_sock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True,prefix="sku",alphabet="12345678900")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural="Productos"
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    def __str__(self):
        return self.title
    def get_precentage(self):
        if(self.old_price>0):
            new_price = round((self.price / self.old_price)*100,0)
        else:
            new_price=0
        return new_price
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images",default="product.jpg")
    product = models.ForeignKey(Product,related_name="p_images", on_delete=models.RESTRICT)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="Imaganes de Productos"
class CartOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    full_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    price = models.DecimalField(max_digits= 12,  decimal_places=2,default="0.00")
    saved = models.DecimalField(max_digits= 12,  decimal_places=2,default="0.00")
    coupons = models.ManyToManyField("core.Coupon",blank=True)
    shipping_method = models.CharField(max_length=255,null=True,blank=True)
    tracking_id = models.CharField(max_length=255,null=True,blank=True)
    tracking_website_address = models.CharField(max_length=255,null=True,blank=True)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE,default="Procesando",blank=True,null=True)
    sku = ShortUUIDField(null=True,blank=True,length=5,prefix="SKU",max_length=20,alphabet="1234567890")
    oid = ShortUUIDField(null=True,blank=True,length=5,max_length=20,alphabet="1234567890")
    stripe_payment_intent = models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        verbose_name_plural="Carrito"
class CartOrderProducts(models.Model):
    order = models.ForeignKey(CartOrder,on_delete=models.RESTRICT)
    invoice_no = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits= 12,decimal_places=2,default=0)
    total = models.DecimalField(max_digits= 12,decimal_places=2,default=0)
    class Meta:
        verbose_name_plural="Carrito Detalle"
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    def order_img(self):
        return mark_safe('<img src="media/%s" width="50" height="50"/>' % (self.image))
class ProductReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.RESTRICT,null=False)
    product = models.ForeignKey(Product,on_delete=models.RESTRICT,null=False,related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING,default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Revisiones de Productos"
    
    def __str__(self):
        return self.title
    def get_rating(self):
        return self.rating
class wishlist_model(models.Model):
    user = models.ForeignKey(User,on_delete=models.RESTRICT,null=False)
    product = models.ForeignKey(Product,on_delete=models.RESTRICT,null=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Lista de deseos"
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.RESTRICT,null=False)
    mobile = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural="Direcciones"
class Coupon(models.Model):
    code =models.CharField(max_length=50)
    discount = models.IntegerField(default=0)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.code
class Blog(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,default="titulo")
    contenido =CKEditor5Field(config_name='extends', null=True, blank=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to="blogs",default='default.jpg')
    
    class Meta:
        verbose_name_plural="Blogs"
    def __str__(self):
        return self.contenido