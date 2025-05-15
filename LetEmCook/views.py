from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Recipe, Comment, Profile
from .forms import RecipeForm, CommentForm, SearchForm
from django.contrib.auth.models import User
from taggit.models import Tag
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta, timezone as std_timezone  # Import standard timezone
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector

import json
import traceback
import google.generativeai as genai
import random

#Authentication and registration views
def welcome_page(request):
    return render(request, 'LetEmCook/welcome.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'LetEmCook/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('email_mfa')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'LetEmCook/login.html')

    return render(request, 'LetEmCook/login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'LetEmCook/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'LetEmCook/login.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'LetEmCook/login.html')

        User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')  # Use the correct namespaced URL here

    return render(request, 'LetEmCook/register.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('welcome')

# ------------------ Email MFA views ------------------

@login_required
def email_mfa_view(request):
    user = request.user

    # Initialize MFA session vars
    if 'email_mfa_code' not in request.session or is_code_expired(request):
        generate_and_send_email_code(request, user)

    if request.method == 'POST':
        entered_code = request.POST.get('code', '').strip()

        if entered_code == request.session.get('email_mfa_code') and not is_code_expired(request):
            request.session['email_mfa_passed'] = True
            clear_mfa_session(request)
            messages.success(request, 'Email verification successful!')

            return redirect('home') 
        else:
            messages.error(request, 'Invalid or expired code. Please try again.')
            return render(request, 'LetEmCook/email_mfa.html')

    return render(request, 'LetEmCook/email_mfa.html')

# ------------------ Helper functions ------------------

def generate_6_digit_code():
    return '{:06d}'.format(random.randint(0, 999999))

def generate_and_send_email_code(request, user):
    code = generate_6_digit_code()
    request.session['email_mfa_code'] = code
    request.session['email_mfa_created_at'] = timezone.now().isoformat()

    send_mail(
        'Your Let Em Cook Verification Code',
        f'Your verification code is: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

def is_code_expired(request):
    created_at_str = request.session.get('email_mfa_created_at')
    if not created_at_str:
        return True
    created_at = datetime.fromisoformat(created_at_str)  # Use datetime's fromisoformat
    created_at = created_at.replace(tzinfo=std_timezone.utc)  # Ensure timezone-aware
    return timezone.now() > created_at + timedelta(minutes=5)

def clear_mfa_session(request):
    request.session.pop('email_mfa_code', None)
    request.session.pop('email_mfa_created_at', None)

@login_required
def home(request):
    # Only allow if MFA has been passed
    if not request.session.get('email_mfa_passed'):
        return redirect('email_mfa') 
    
    recipes = Recipe.objects.all().order_by('-created_at')
    #profile = get_object_or_404(Profile, user=request.user)
    for recipe in recipes:
        recipe.ingredient_list = [i.strip() for i in recipe.ingredients.split(',')]

    form = RecipeForm()

    trending_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:20]

    return render(request, 'LetEmCook/home.html', {'recipes': recipes, 'form': form, 'trending_tags': trending_tags})

#@login_required
def profile(request, profile_username):
    profile = get_object_or_404(Profile, user__username =profile_username)
    recipes = Recipe.objects.filter(user = profile.user).order_by('-created_at')
    for recipe in recipes:
        recipe.ingredient_list = [i.strip() for i in recipe.ingredients.split(',')]
    friends = profile.friendship.all()
    return render(request, 'LetEmCook/profile.html', {'profile': profile, 'recipes': recipes, 'friends': friends})

def recipe(request, recipe_id, slug=None):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.ingredient_list = [i.strip() for i in recipe.ingredients.split(',')]

    commentForm = CommentForm()
    recipeForm = RecipeForm()

    comments = recipe.comments.all()
    return render(request, 'LetEmCook/recipe.html', {'recipe': recipe, 'comments': comments, 'commentForm': commentForm, 'recipeForm': recipeForm})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        tags = request.POST.get('tags', '')
        image = request.FILES.get('image', None)
        recipe = Recipe.objects.create(
            user=request.user,
            title=title,
            description=description,
            ingredients=ingredients,
            image=image
        )
        recipe.tags.add(*[tag.strip() for tag in tags.split(',') if tag])

        recipe.save()
        return redirect('recipe_detail', recipe_id=recipe.id, slug=recipe.slug)    

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "Recipe deleted successfully.")
        return redirect('home')

@login_required
def add_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        content = request.POST['content']
        image = request.FILES.get('image', None)
        Comment.objects.create(recipe=recipe, user=request.user, content=content, image=image)

        return redirect('recipe_detail', recipe_id=recipe.id, slug=recipe.slug)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        recipe_id = comment.recipe.id
        recipe_slug = comment.recipe.slug
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('recipe_detail', recipe_id=recipe_id, slug=recipe_slug)

#@login_required
def add_friend(request, user_id):
    friend_user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    friend_profile = get_object_or_404(Profile, user=friend_user)
    profile.friendship.add(friend_profile)
    return redirect('profile')

#@login_required
def remove_friend(request, user_id):
    friend_user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    friend_profile = get_object_or_404(Profile, user=friend_user)
    profile.friendship.remove(friend_profile)
    return redirect('profile')

def search(request):
    query = request.GET.get('q', '')

    results = Recipe.objects.none()
    
    if query.startswith('#'):
        tag = query[1:]
        results = Recipe.objects.filter(tags__name__icontains=tag).order_by('-created_at')

    elif query.startswith('@'):
        username = query[1:]
        results = Recipe.objects.filter(user__username__icontains=username).order_by('-created_at')

    else:
        results = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(user__username__icontains=query)
        ).order_by('-created_at')

    for recipe in results:
        recipe.ingredient_list = [i.strip() for i in recipe.ingredients.split(',')]

    return render(request, 'LetEmCook/search.html', {'results': results, 'query': query})

def tagged_recipes(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    recipes = Recipe.objects.filter(tags__name__in=[tag_name])
    return render(request, 'search.html', {'recipes': recipes, 'tag': tag})

@login_required
def edit_bio(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.bio = request.POST['bio']
        profile.save()
        return redirect('profile')

@login_required
def edit_profile_picture(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.profile_picture = request.FILES.get('profile_picture', profile.profile_picture)
        profile.save()
        return redirect('profile')

@login_required
@csrf_exempt
def generate_description(request):
    if request.method == 'POST':
        genai.configure(api_key=settings.GEMINI_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        prompt = f"You are a fun, creative, and a friendly AI chef/cook. Generate a creative recipe description for a dish called {title} with the following ingredients: {ingredients}. Please provide a detailed description and instructions. Make it engaging and appetizing. Do not use any markdown formatting and just use plain, natural language suitable for pasting in notepad. Separate into paragraphs/new lines if necessary per each section/line. Still use numbering or bullets if necessary. Do not return any explanation of the prompt. Do not return who you are."
        
        try:
            bot_response = model.generate_content(prompt)
            description = bot_response.text.strip()
            if not description:
                return JsonResponse({'error': 'No description generated'}, status=500)
            
            return JsonResponse({'description': description})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def generate_tags(request):
    if request.method == 'POST':
        genai.configure(api_key=settings.GEMINI_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        prompt = f"Do not return any explanation, just the string that contains the tags that are comma-separated.Generate SEO-friendly product tags (comma-separated). Generate tags for a recipe called {title} with the following ingredients: {ingredients}. The description of the recipe is: {description}. "
        
        try:
            bot_response = model.generate_content(prompt)
            tags = bot_response.text.strip()
            print(tags)
            if not tags:
                return JsonResponse({'error': 'No tags generated'}, status=500)
            return JsonResponse({'tags': tags})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
