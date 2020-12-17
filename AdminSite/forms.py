from django import forms
from store.models.category import Category
from store.models.product import Product

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
            })
        }
        labels = {
        "name": ""
        }


# class AddProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
