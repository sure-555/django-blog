from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate

from alpha.models import Category, Post

class contactForm(forms.Form):
    name=forms.CharField(label="Name",max_length=100)
    email=forms.EmailField(label="E-mail")
    message=forms.CharField(label="Message")

class registerForm(forms.ModelForm):
    username=forms.CharField(label="Username",max_length=100,required=True)
    email=forms.EmailField(label="E-mail",required=True)
    password=forms.CharField(label="Password",max_length=100,required=True)
    password_confirm=forms.CharField(label="Confirm Password",max_length=100,required=True)

    class Meta:
        model=User
        fields=['username','email','password']
    
    def clean(self):
        self.cleaned_data=super().clean()
        password=self.cleaned_data.get("password")
        password_confirm=self.cleaned_data.get("password_confirm")
    
        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError("Passwords did not match")


class loginForm(forms.Form):
    username=forms.CharField(label="Username",max_length=100,required=True)
    password=forms.CharField(label="Password",max_length=100,required=True)

    def clean(self):
        self.cleaned_data=super().clean()
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        if password and username:
            user=authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError("User doesn't exist")
            
class ForgotPassword(forms.Form):
    email=forms.EmailField(label="E-mail",required=True)

    def clean(self):
        cleaned_data=super().clean()
        email=cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No User Registered with this email")
        
class ResetPassword(forms.Form):
    new_password=forms.CharField(label="Password",max_length=100,required=True)
    password_confirm=forms.CharField(label="Confirm Password",max_length=100,required=True)

    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get("new_password")
        password_confirm=cleaned_data.get("password_confirm")
    
        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError("Passwords did not match")

        return(cleaned_data)

class PostForm(forms.ModelForm):
    title=forms.CharField(label="Title",max_length=200,required=True)
    content=forms.CharField(label="Content",required=True)
    category=forms.ModelChoiceField(label="Category",required=True,queryset=Category.objects.all())
    image=forms.ImageField(label="Image",required=False)

    class Meta:
        model=Post
        fields=['title','content','category','image']

    def clean(self):
        cleaned_data=super().clean()
        title=cleaned_data.get('title')
        content=cleaned_data.get('content')
        

        #custom validation
        if title and len(title)<5:
            raise forms.ValidationError("Title should contain atleast 5 characters")
        if content and len(content)<10:
            raise forms.ValidationError("Content should contain atleast 10 characters")
        
    def save(self,commit= ...):
        cleaned_data=super().clean()
        image=cleaned_data.get('image')
        post=super().save(commit)
        
        if image:   
            post.image=image
        else:
            image_url="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
            post.image=image_url
        if commit:
            post.save()

        return post