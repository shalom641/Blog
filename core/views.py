from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Blog, Post, Comment
from .forms import PostForm, RegistrationForm, UserLoginForm, CommentForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages  
from .forms import ContactForm

# ----- Static Pages -----
@login_required
def location(request):
    return render(request, 'location.html')


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def contact(request):
    return render(request, 'contact.html')



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"New Contact Form Submission from {form.cleaned_data['name']}"
            body = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            
            send_mail(
                subject,
                body,
                sender,
                ['sakalashalomt@gmail.com'],  # Replace with your email
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})




@login_required
def test(request):
    return render(request, 'test.html')


# ----- Blog Home -----
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


# ----- Blog Detail -----
@login_required
def detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'detail.html', {'blog': blog})


# ----- User Registration -----
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('core:home')  # Fixed to redirect correctly
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# ----- User Login -----
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(86400 * 30) 
                return redirect('core:home')  # Fixed to redirect after login
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


# ----- Logout -----
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Fixed the redirect to login page


# ----- Profile -----
@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})


# ----- All Posts -----
@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


# ----- Single Post Detail with Comments -----
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('core:post_detail', pk=post.pk)  # Fixed redirect
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})


# ----- Create New Post -----
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Include request.FILES for image handling
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('core:post_detail', pk=post.pk)  # Redirect to the newly created post
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})


# ----- Edit Post -----
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Allow file updates as well
        if form.is_valid():
            form.save()
            return redirect('core:post_detail', pk=post.pk)  # Redirect to the edited post detail
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})


# ----- Delete Post -----
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('core:post_list')  # Redirect to the post list after deletion
    return render(request, 'post_confirm_delete.html', {'post': post})


# ----- AJAX Add Comment -----
@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)  # Fixed undefined variable issue
        comment = Comment.objects.create(post=post, author=request.user, content=content)
        return JsonResponse({
            'comment_id': comment.id,
            'author': request.user.username,
            'content': comment.content
        })


# ----- AJAX Toggle Comment Like -----
@login_required
def increaselikes(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Remove the like if already liked
    else:
        post.likes.add(request.user)  # Add a like if not liked
    return redirect('core:home')  # Fixed redirect to home page
