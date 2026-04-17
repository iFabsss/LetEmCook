
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import SignupView

urlpatterns = [
    # Main app routes
    path('', include('LetEmCook.urls')),

    # Admin
    path('admin/', admin.site.urls),

    # Authentication (Django Allauth)
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', SignupView.as_view(template_name='accounts/signup.html'), name='signup'),

    # ✅ API routes (NEW)
    path('api/', include('LetEmCook.api_urls')),
]

# Media files (for images/uploads)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

