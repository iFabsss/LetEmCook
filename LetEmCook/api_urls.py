from django.urls import path
from . import api_views

urlpatterns = [
    # Recipes
    path('recipes/', api_views.get_recipes),
    path('recipes/<int:pk>/', api_views.get_recipe),
    path('recipes/create/', api_views.create_recipe),

    # Comments
    path('comments/', api_views.get_comments),

    # Profiles
    path('profiles/', api_views.get_profiles),

    #User
    path('users/', api_views.get_users),
    path('users/<int:pk>/', api_views.get_user),

    
]