# ===== ARCHIVO: actions.py (ACTUALIZADO) =====
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from db_productos import (
    consultar_precio_producto, 
    disponibilidad_producto, 
    tiene_descuento,
    obtener_todos_productos,
    buscar_producto_especifico
)

class ActionConsultarPrecio(Action):
    def name(self) -> Text:
        return "action_consultar_precio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        producto = tracker.get_slot("producto")
        
        if not producto:
            dispatcher.utter_message(text="¿De qué producto te gustaría conocer el precio? Tenemos proteína, creatina y multivitamínico.")
            return []
        
        resultado = consultar_precio_producto(producto)
        
        if resultado["encontrado"]:
            mensaje = f"💰 **Precios de {resultado['categoria']}:**\n\n"
            
            for prod in resultado["productos"]:
                if prod["descuento"] > 0:
                    mensaje += f"• **{prod['nombre']}**\n"
                    mensaje += f"  ~~${prod['precio_original']:,}~~ ➜ **${prod['precio_final']:,}** "
                    mensaje += f"({prod['descuento']}% OFF) 🎉\n"
                    mensaje += f"  Stock: {prod['stock']} unidades\n\n"
                else:
                    mensaje += f"• **{prod['nombre']}**\n"
                    mensaje += f"  **${prod['precio_final']:,}**\n"
                    mensaje += f"  Stock: {prod['stock']} unidades\n\n"
            
            mensaje += "🚚 Envío disponible a Bucaramanga"
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text=f"Lo siento, no encontré información sobre '{producto}'. ¿Te refieres a proteína, creatina o multivitamínico?")
        
        return [SlotSet("producto", None)]

class ActionConsultarDisponibilidad(Action):
    def name(self) -> Text:
        return "action_consultar_disponibilidad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        producto = tracker.get_slot("producto")
        
        if not producto:
            dispatcher.utter_message(text="¿Qué producto quieres consultar? Tenemos proteína, creatina y multivitamínico disponibles.")
            return []
        
        resultado = disponibilidad_producto(producto)
        
        if resultado["encontrado"]:
            mensaje = f"📦 **Disponibilidad de {resultado['categoria']}:**\n\n"
            
            for prod in resultado["productos"]:
                mensaje += f"• **{prod['nombre']}**\n"
                mensaje += f"  {prod['estado']} - {prod['stock']} unidades\n\n"
            
            mensaje += "🚚 Todos los productos disponibles se envían a Bucaramanga"
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text=f"No encontré información sobre '{producto}'. ¿Te refieres a proteína, creatina o multivitamínico?")
        
        return [SlotSet("producto", None)]

class ActionConsultarDescuento(Action):
    def name(self) -> Text:
        return "action_consultar_descuento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        producto = tracker.get_slot("producto")
        
        if not producto:
            dispatcher.utter_message(text="¿Para qué producto quieres saber sobre descuentos? Tengo ofertas especiales en proteína, creatina y multivitamínico.")
            return []
        
        resultado = tiene_descuento(producto)
        
        if resultado["encontrado"]:
            mensaje = f"🎯 **Descuentos en {resultado['categoria']}:**\n\n"
            
            productos_con_descuento = []
            productos_sin_descuento = []
            
            for prod in resultado["productos"]:
                if prod["tiene_descuento"]:
                    productos_con_descuento.append(prod)
                else:
                    productos_sin_descuento.append(prod)
            
            if productos_con_descuento:
                mensaje += "🎉 **¡CON DESCUENTO!**\n"
                for prod in productos_con_descuento:
                    mensaje += f"• **{prod['nombre']}**\n"
                    mensaje += f"  {prod['porcentaje']}% OFF: ~~${prod['precio_original']:,}~~ ➜ **${prod['precio_descuento']:,}**\n\n"
            
            if productos_sin_descuento:
                mensaje += "💼 **Precio regular:**\n"
                for prod in productos_sin_descuento:
                    mensaje += f"• **{prod['nombre']}**: ${prod['precio_original']:,}\n"
            
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text=f"No encontré información sobre '{producto}'. ¿Te refieres a proteína, creatina o multivitamínico?")
        
        return [SlotSet("producto", None)]

class ActionMostrarCatalogo(Action):
    def name(self) -> Text:
        return "action_mostrar_catalogo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        productos = obtener_todos_productos()
        
        mensaje = "🛍️ **Catálogo SupleMax - Productos Disponibles:**\n\n"
        
        categoria_actual = ""
        for prod in productos:
            if prod["categoria"] != categoria_actual:
                categoria_actual = prod["categoria"]
                mensaje += f"**--- {categoria_actual} ---**\n"
            
            estado = "✅ Disponible" if prod["disponible"] else "❌ Agotado"
            
            if prod["descuento"] > 0:
                mensaje += f"• **{prod['nombre']}** 🎉\n"
                mensaje += f"  ~~${prod['precio_original']:,}~~ ➜ **${prod['precio_final']:,}** ({prod['descuento']}% OFF)\n"
                mensaje += f"  {estado} ({prod['stock']} unidades)\n\n"
            else:
                mensaje += f"• **{prod['nombre']}**\n"
                mensaje += f"  **${prod['precio_final']:,}**\n"
                mensaje += f"  {estado} ({prod['stock']} unidades)\n\n"
        
        mensaje += "🚚 **Envío disponible solo a Bucaramanga**\n"
        mensaje += "💬 Pregúntame por categorías específicas para más detalles!"
        
        dispatcher.utter_message(text=mensaje)
        return []

class ActionInformacionEnvio(Action):
    def name(self) -> Text:
        return "action_informacion_envio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mensaje = "🚚 **Información de Envío:**\n\n"
        mensaje += "📍 **Cobertura:** Solo realizamos envíos a Bucaramanga y área metropolitana\n"
        mensaje += "⏰ **Tiempo de entrega:** 1-2 días hábiles\n"
        mensaje += "💰 **Costo de envío:** $8.000 (GRATIS en compras superiores a $100.000)\n"
        mensaje += "📞 **Contacto:** Una vez realices el pedido, te contactaremos para confirmar dirección\n\n"
        mensaje += "¿Te interesa algún producto en particular?"
        
        dispatcher.utter_message(text=mensaje)
        return []

class ActionConsultarPrecioEspecifico(Action):
    def name(self) -> Text:
        return "action_consultar_precio_especifico"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        producto_especifico = tracker.get_slot("producto_especifico")
        
        if not producto_especifico:
            dispatcher.utter_message(text="¿Qué producto específico te interesa?")
            return []
        
        resultado = buscar_producto_especifico(producto_especifico)
        
        if resultado["encontrado"]:
            mensaje = f"🎯 **{resultado['nombre']}**\n\n"
            if resultado["descuento"] > 0:
                mensaje += f"💰 ~~${resultado['precio_original']:,}~~ ➜ **${resultado['precio_final']:,}** ({resultado['descuento']}% OFF)\n"
            else:
                mensaje += f"💰 **${resultado['precio_final']:,}**\n"
            mensaje += f"📦 Stock: {resultado['stock']} unidades"
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text=f"No encontré '{producto_especifico}'")
        
        return [SlotSet("producto_especifico", None)]