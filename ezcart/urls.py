from django.contrib import admin
from django.urls import path,include
import User

from ezcart import settings
from .import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('store/',include('store.urls')),
    path('cart/',include('cart.urls')),
    path('accounts/',include('User.urls')),
    path('orders/',include('order.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
