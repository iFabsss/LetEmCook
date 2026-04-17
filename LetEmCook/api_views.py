from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe, Comment, Profile
from .serializers import RecipeSerializer, CommentSerializer, ProfileSerializer


# =====================
# RECIPES
# =====================

# GET all recipes
@api_view(['GET'])
def get_recipes(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


# GET single recipe
@api_view(['GET'])
def get_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)


# =====================
# COMMENTS
# =====================

@api_view(['GET'])
def get_comments(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


# =====================
# PROFILES
# =====================

@api_view(['GET'])
def get_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)