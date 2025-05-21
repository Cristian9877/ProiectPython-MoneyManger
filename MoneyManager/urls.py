from django.contrib.admin import views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path, include
from django.contrib.auth import views
from userextend.forms import AuthenticationForm, AuthenticationNewForm
from django.contrib import admin

urlpatterns = [
         #path('admin/', admin.site.urls),
         path('', include('home.urls')),
         path('intro/', include('intro.urls')),
    path("login/",
         views.LoginView.as_view(template_name='registration/login.html', form_class=AuthenticationNewForm),
         name="login"),
         path('',include('django.contrib.auth.urls')),
         path('',include('userextend.urls')),
         path('',include('transaction.urls')),
]
