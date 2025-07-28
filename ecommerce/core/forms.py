from stripe import Review
from django import forms
from core.models import ProductReview,Blog

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Escribe tu Revision'}))
    class Meta:
        model = ProductReview
        fields = ['review','rating']
class BlogForm(forms.ModelForm):
    blog = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Escribe el Blog'}))
    class Meta:
        model = Blog
        fields= ['contenido','status']