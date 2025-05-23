"""
URL configuration for Let_Em_Cook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from allauth.account.views import SignupView

urlpatterns = [
    path('', include('LetEmCook.urls')),  # Include the URLs from the LetEmCook app
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Social auth
    path('accounts/signup/', SignupView.as_view(template_name='accounts/signup.html'), name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
