from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome_page, name='welcome'),  # Home page
    path('login/', views.login_page, name='login'),  # Login page
    path('register/', views.register_page, name='register'),  # Register page
    path('email_mfa/', views.email_mfa_view, name='email_mfa'),  # Email MFA page
    path('account/signup/', include('allauth.account.urls')),  # Allauth signup
    path('logout', views.logout_user, name='logout'),

    path('home', views.home, name='home'),
    path('profile/@<str:profile_username>', views.profile, name='profile'),
    path('recipe/<int:recipe_id>/<slug:slug>', views.recipe, name='recipe_detail'),
    path('generateDescription', views.generate_description, name='generate_description'),
    path('generateTags', views.generate_tags, name='generate_tags'),
    path('addRecipe', views.add_recipe, name='add_recipe'), 
    #path('edit_recipe/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),
    path('deleteRecipe/<int:recipe_id>', views.delete_recipe, name='delete_recipe'),
    path('addComment/<int:recipe_id>', views.add_comment, name='add_comment'),
    #path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('deleteComment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    #path('add_friend/<int:user_id>', views.add_friend, name='add_friend'),
    #path('remove_friend/<int:user_id>', views.remove_friend, name='remove_friend'),
    path('search', views.search, name='search'),
    #path('tag/<slug:tag_slug>', views.tagged_recipes, name='tagged_recipes'),
    #path('edit_bio', views.edit_bio, name='edit_bio'),
    #path('edit_profile_picture', views.edit_profile_picture, name='edit_profile_picture'),
]
