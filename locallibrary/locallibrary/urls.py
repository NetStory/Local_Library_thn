"""
URL configuration for locallibrary project.

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

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.conf.urls import include

urlpatterns += [    # 这样写是为了区分新旧代码
    path('catalog/', include('catalog.urls')),  # 这他妈是在干啥 这就是 include() 的核心：切掉已经匹配的前缀，把剩下的路径继续向下传递。
    # 只要URL以 catlog/ 开头，后面部分交给 catalog/urls.py继续判断
]

from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]