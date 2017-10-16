from django import forms
from rest_framework.exceptions import ValidationError
from blog.models import PostImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('blog_post', 'image', 'title')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 4 * 1024 * 768:
                raise ValidationError("Image file too large")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")