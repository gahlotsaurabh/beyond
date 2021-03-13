from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FileViewSet

router = routers.DefaultRouter()

router.register(r'file', FileViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]


# urlpatterns = [
#     path('', views.apt_root),
#     path('comments/', views.comment_list),
#     path('comments/<int:pk>/', views.comment_detail)
# ]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
