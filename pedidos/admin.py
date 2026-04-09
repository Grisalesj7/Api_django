from django.contrib import admin
from .models import Producto, Cliente, HistorialStock

# Borramos los "admin.site.register" simples para evitar errores de duplicado
admin.site.register(Cliente)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Asegúrate de que estos nombres coincidan con los de tu models.py
    list_display = ('nombre', 'precio', 'stock_actual') 
    search_fields = ('nombre',)

@admin.register(HistorialStock)
class HistorialStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'tipo', 'fecha')
    list_filter = ('tipo', 'fecha')


# Register your models here.
