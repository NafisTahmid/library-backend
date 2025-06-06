from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('base.urls'))
    path('api/products/', include('base.urls.products_urls')),
    path('api/users/', include('base.urls.users_urls')),
    path('api/orders/', include('base.urls.orders_urls')),
    path('api/wishlist/', include('base.urls.wishlist_urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)