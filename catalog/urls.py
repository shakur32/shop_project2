from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'catalog'

# Роутер для API (Задачи)
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    # --- МАГАЗИН (Твои товары и корзина) ---
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # --- БЛОГ (Публикации) ---
    path('publications/', views.PublicationListView.as_view(), name='publication_list'),
    path('publication/<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('publication/create/', views.PublicationCreateView.as_view(), name='publication_create'),
    path('publication/<int:pk>/update/', views.PublicationUpdateView.as_view(), name='publication_update'),
    path('publication/<int:pk>/delete/', views.PublicationDeleteView.as_view(), name='publication_delete'),
    path('publication/<int:pk>/like/', views.AddLikeView.as_view(), name='add_like'),

    # --- REST API (Для задания) ---
    path('api/', include(router.urls)),
    path('api/register/', views.UserCreateView.as_view({'post': 'create'})),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]