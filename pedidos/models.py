from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre
    
class HistorialStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField() # +5 o -5
    tipo = models.CharField(max_length=20) # 'VENTA', 'CANCELACION', 'INGRESO'
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha.strftime('%d/%m %H:%M')} - {self.producto.nombre}: {self.cantidad} ({self.tipo})"
    
class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Validación antes de guardar el detalle
        if self.producto.stock < self.cantidad:
            raise ValueError("Stock insuficiente")
        
        self.subtotal = self.cantidad * self.producto.precio
        super().save(*args, **kwargs)

# --- SEÑALES PARA AUTOMATIZAR EL STOCK ---

# --- SEÑALES PARA AUTOMATIZAR EL STOCK ---

@receiver(post_save, sender=DetallePedido)
def actualizar_stock_y_total(sender, instance, created, **kwargs):
    if created:
        # 1. Restar del stock
        producto = instance.producto
        producto.stock -= instance.cantidad
        producto.save(update_fields=['stock'])

        # 2. GUARDAR EN HISTORIAL (Añade esto)
        HistorialStock.objects.create(
            producto=producto,
            cantidad=-instance.cantidad, # Negativo porque sale stock
            tipo='VENTA'
        )

    # Actualizar el total del pedido principal
    pedido = instance.pedido
    nuevo_total = pedido.detalles.aggregate(total=models.Sum('subtotal'))['total'] or 0
    pedido.total_pagado = nuevo_total
    pedido.save(update_fields=['total_pagado'])
    print(f"💰 Pedido #{pedido.id} actualizado. Total: ${nuevo_total}")

# --- 2. SEÑAL PARA DEVOLVER STOCK SI SE ELIMINA EL DETALLE ---
@receiver(post_delete, sender=DetallePedido)
def devolver_stock_al_eliminar(sender, instance, **kwargs):
    # 1. Devolver unidades al inventario
    producto = instance.producto
    producto.stock += instance.cantidad
    producto.save(update_fields=['stock'])
    
    # 2. GUARDAR EN HISTORIAL (Añade esto)
    HistorialStock.objects.create(
        producto=producto,
        cantidad=instance.cantidad, # Positivo porque regresa stock
        tipo='CANCELACION'
    )
    
    # Recalcular el total del pedido
    pedido = instance.pedido
    nuevo_total = pedido.detalles.aggregate(total=models.Sum('subtotal'))['total'] or 0
    pedido.total_pagado = nuevo_total
    pedido.save(update_fields=['total_pagado'])
    
    print(f"🔄 Stock devuelto a {producto.nombre}. Nuevo total pedido: ${nuevo_total}")