from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Магазин
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    
    # Публикации
    path('publications/', views.PublicationListView.as_view(), name='publication_list'),
    path('publication/<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('publication/add/', views.PublicationCreateView.as_view(), name='publication_create'),
    path('publication/<int:pk>/update/', views.PublicationUpdateView.as_view(), name='publication_update'),
    path('publication/<int:pk>/delete/', views.PublicationDeleteView.as_view(), name='publication_delete'),
    path('publication/<int:pk>/like/', views.AddLikeView.as_view(), name='add_like'),
]