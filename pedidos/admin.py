from django.contrib import admin
from .models import Producto, Cliente, HistorialStock, Pedido, DetallePedido

# Registro simple para Cliente
admin.site.register(Cliente)

# Configuración para ver los productos de un pedido dentro del mismo pedido (Inline)
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'estado', 'total_pagado')
    list_filter = ('estado', 'fecha')
    inlines = [DetallePedidoInline] # Esto permite añadir productos al pedido ahí mismo

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Cambié 'stock_actual' por 'stock' para que coincida con tu models.py
    list_display = ('nombre', 'precio', 'stock') 
    search_fields = ('nombre',)

@admin.register(HistorialStock)
class HistorialStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'tipo', 'fecha')
    list_filter = ('tipo', 'fecha')