from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Category, Post,AboutUs
from django.core.paginator import Paginator
from .form import ForgotPassword, PostForm, ResetPassword, contactForm,registerForm,loginForm
import logging
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied

def index(request):
    project = "ALPHA"
    
    # 1. Grab all published posts
    all_posts = Post.objects.filter(is_piublished=True).order_by('-created_at')
    
    # 2. Extract the search keyword from the homepage input box
    search_query = request.GET.get('search')
    if search_query:
        # Filters titles containing the searched words, ignoring case differences
        all_posts = all_posts.filter(title__icontains=search_query)
    
    # 3. Pass the (potentially filtered) posts into your paginator
    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    # 4. Pass the search_query to the template context so the input field can reference it
    context = {
        'name': project,
        'page_obj': page_object,
        'search_query': search_query
    }
    
    return render(request, 'index.html', context)


def about(request):
    if request.user and not request.user.has_perm('alpha.view_post'):
        messages.error(request, 'You have no permission to view any post')
        return redirect('alpha:index')
    
    # Safely get the first record object
    about_record = AboutUs.objects.first()
    
    # If the database has content, grab it; otherwise, display a friendly fallback string
    if about_record:
        content = about_record.content
    else:
        content = "About Us content is currently being updated."
        
    return render(request, 'about.html', {'content': content})

def post(request,slug):
    #by the post list
    #post=next((item for item in posts if item['id']==post_id),None)
    post=Post.objects.get(slug=slug)
    related_posts=Post.objects.filter(category=post.category).exclude(pk=post.id)
    return render(request,'base.html',{'post':post,'related_posts':related_posts})

def contact(request):
    if request.method =='POST':
        form=contactForm(request.POST)
        if form.is_valid():
            logger=logging.getLogger("TESTING")
            logger.debug(f"POST data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}")
            success="Your mail has been sent"
            return render(request,'contact.html',{'success':success})
    return render(request,'contact.html')

def register(request):
    form=registerForm()
    if request.method =='POST':
        form=registerForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            #add  user to reader group
            readers_group,created=Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            messages.success(request,"Registration Sucessfull,You can login")
            return redirect("alpha:login")

    return render(request,'register.html',{'form':form})

def login(request):
    form=loginForm()
    if request.method =='POST':
        form=loginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('alpha:dashboard')
            
    return render(request,'login.html',{'form':form})

def dashboard(request):
    title="My Posts"
    #getting user posts
    all_post=Post.objects.filter(user=request.user)
    paginator=Paginator(all_post,6)
    page_number=request.GET.get('page')
    page_object=paginator.get_page(page_number)
    return render(request,'dashboard.html',{'title':title,'page_obj':page_object    })

def logout(request):
    auth_logout(request)
    return redirect("alpha:index")

def forgot_password(request):
    form=ForgotPassword()
    if request.method =='POST':
        form=ForgotPassword(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            #send reset email
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            current_site=get_current_site(request)
            domain=current_site.domain
            subject="Reset Password Requested"
            message=render_to_string('reset_password_email.html',{"domain":domain,"uid":uid,"token":token})
            send_mail(subject,message,'noreply@gmail.com',[email])
            messages.success(request,"Email has been sent")

    return render(request,'forgot_password.html',{"form":form}) 

def reset_password(request,uidb64,token):
    form=ResetPassword()
    if request.method =='POST':
        form=ResetPassword(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,"Your password has been reset seccessfully")
                return redirect('alpha:login')
            else:
                messages.error(request,"The password reset link is invalid")

    return render(request,'reset_password.html',{'form':form})


@login_required
def new_post(request):
    is_reader = request.user.groups.filter(name='Readers').exists()
    has_perm = request.user.has_perm('alpha.add_post')
    
    if not (is_reader or has_perm):
        raise PermissionDenied  
        
    category = Category.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            
            # --- BINARY IMAGE CONVERSION LOGIC ---
            if 'image' in request.FILES:
                uploaded_file = request.FILES['image']
                post.image_data = uploaded_file.read()  # Read raw file bytes
                post.image_mime_type = uploaded_file.content_type  # Save file type (PNG/JPEG)
            # --------------------------------------
            
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('alpha:dashboard')
    else:
        form = PostForm()
        
    return render(request, 'new_post.html', {'categories': category, 'form': form})
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # OWNERSHIP SECURITY: Only allow the author or a superuser to edit
    if post.user != request.user and not request.user.is_superuser:
        raise PermissionDenied
        
    category = Category.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Don't save to the database immediately
            updated_post = form.save(commit=False)
            
            # --- BINARY IMAGE CONVERSION FOR EDITING ---
            if 'image' in request.FILES:
                uploaded_file = request.FILES['image']
                updated_post.image_data = uploaded_file.read()  # Read new file bytes
                updated_post.image_mime_type = uploaded_file.content_type  # Update file type
            # --------------------------------------------
            
            updated_post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('alpha:dashboard')
    else:
        form = PostForm(instance=post)
        
    return render(request, 'edit_post.html', {'categories': category, 'post': post, 'form': form})
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # OWNERSHIP SECURITY: Only allow the author or a superuser to delete
    if post.user != request.user and not request.user.is_superuser:
        raise PermissionDenied
        
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('alpha:dashboard')


@login_required
def publish_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # OWNERSHIP SECURITY: Only allow the author or a superuser to publish
    if post.user != request.user and not request.user.is_superuser:
        raise PermissionDenied
        
    post.is_piublished = True  # Corrected typo from your original 'is_piublished'
    post.save()
    messages.success(request, 'Post published successfully!')
    return redirect('alpha:dashboard')   


import base64

