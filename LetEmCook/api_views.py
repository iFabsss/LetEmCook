from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe, Comment, Profile, User
from .serializers import RecipeSerializer, CommentSerializer, ProfileSerializer, UserSerializer


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


# CREATE recipe
@api_view(['POST'])
def create_recipe(request):
    serializer = RecipeSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)


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


# =====================
# USERS ✅
# =====================

# GET all users
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# GET single user
@api_view(['GET'])
def get_user(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)