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


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control',})
        self.fields['name'].label = ''
        self.fields['price'].widget.attrs.update({'class':'form-control',})
        self.fields['unit'].widget.attrs.update({'class':'form-control',})
        self.fields['description'].widget.attrs.update({'class':'form-control',})
        self.fields['category'].widget.attrs.update({'class':'form-control text-info',})
        self.fields['image'].widget.attrs.update({'class':'form-control-file border','type':'file'})
        self.fields['image'].label = 'Select your Image'
