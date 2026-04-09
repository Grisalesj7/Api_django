from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ClienteAPI, ProductoAPI, PedidoAPI, DetallePedidoAPI
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    
    # URLs para Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/eliminar/<int:pk>/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # Rutas para exportar individualmente
    path('clientes/pdf/<int:pk>/', views.exportar_cliente_pdf, name='cliente_pdf'),
    path('clientes/excel/<int:pk>/', views.exportar_cliente_excel, name='cliente_excel'),

    # URLs para Productos
    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    # URLs para Pedidos
    path('pedidos/', views.PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/nuevo/', views.PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/editar/<int:pk>/', views.PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedidos/eliminar/<int:pk>/', views.PedidoDeleteView.as_view(), name='pedido_delete'),

    # Rutas de descarga para Productos
    path('productos/pdf/<int:pk>/', views.exportar_producto_pdf, name='producto_pdf'),
    path('productos/excel/<int:pk>/', views.exportar_producto_excel, name='producto_excel'),

    # Rutas de descarga para Pedidos
    path('pedidos/pdf/<int:pk>/', views.exportar_pedido_pdf, name='pedido_pdf'),
    path('pedidos/excel/<int:pk>/', views.exportar_pedido_excel, name='pedido_excel'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
]

# ================= API =================

router = DefaultRouter()
router.register(r'api/clientes', ClienteAPI)
router.register(r'api/productos', ProductoAPI)
router.register(r'api/pedidos', PedidoAPI)
router.register(r'api/detalles-pedidos', DetallePedidoAPI)

urlpatterns += router.urls

# ================= LOGIN =================

urlpatterns += [
    path('api/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
]