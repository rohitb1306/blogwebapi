from django import forms
from .models import Blog



class blogform(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "blog_image",
            "blog_title",
            "blog_keywords",
            "blog_description",
            "blog_content",    
        ]
        widgets = {
            "blog_image": forms.FileInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "blog_title": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "blog_keywords": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "blog_description": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "blog_content": forms.TextInput(
                attrs={"class": "form-control form-control-lg",'maxlength':'150'}
            ),
        }


    #     blog_auther = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    # blog_image = models.ImageField(
    #     upload_to="blog/images", default="blog/images/image.jpg", null=True
    # )
    # blog_content = RichTextField(null=True)
    # blog_title = models.CharField(max_length=150, unique=True)
    # blog_keywords = models.CharField(max_length=150, null=True)
    # blog_description = models.CharField(max_length=150, null=True)
    # blog_uploaded_on = models.DateTimeField(auto_now=True)
    # blog_is_approved = models.BooleanField(default=False)
    # blog_new_request = models.BooleanField(default=True)
    # blog_del_request = models.BooleanField(default=False)