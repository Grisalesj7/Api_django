from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, DetallePedido

# Asegúrate de que esta clase esté escrita TAL CUAL
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        # Agrega aquí los campos que quieres que se vean del pedido
        fields = ['cliente', 'estado'] 

# Este es el conjunto de formularios para los productos
DetallePedidoFormSet = inlineformset_factory(
    Pedido, 
    DetallePedido, 
    fields=['producto', 'cantidad'], 
    extra=3, 
    can_delete=True
)