# ===== ARCHIVO: db_productos.py (VERSIÓN DETALLADA) =====
"""
Base de datos simulada para productos específicos de SupleMax
"""

# Base de datos con productos específicos
PRODUCTOS_DB = {
    "proteina": {
        "categoria": "Proteínas",
        "productos": [
            {
                "nombre": "MuscleTech Whey Protein 2lb",
                "marca": "MuscleTech",
                "peso": "2lb",
                "precio": 120000,
                "stock": 8,
                "descuento": 10,
                "sabores": ["vainilla", "chocolate"],
                "descripcion": "Proteína de suero premium para desarrollo muscular"
            },
            {
                "nombre": "ISO Whey Protein 5lb",
                "marca": "ISO",
                "peso": "5lb",
                "precio": 240000,
                "stock": 5,
                "descuento": 15,
                "sabores": ["chocolate", "fresa", "vainilla"],
                "descripcion": "Proteína isolada de máxima pureza"
            },
            {
                "nombre": "Gold Standard Whey 1lb",
                "marca": "Optimum Nutrition",
                "peso": "1lb",
                "precio": 85000,
                "stock": 12,
                "descuento": 0,
                "sabores": ["chocolate", "vainilla"],
                "descripcion": "El estándar dorado en proteínas"
            }
        ]
    },
    "creatina": {
        "categoria": "Creatinas",
        "productos": [
            {
                "nombre": "Creatina Monohidrato 300g",
                "marca": "Universal",
                "peso": "300g",
                "precio": 45000,
                "stock": 15,
                "descuento": 12,
                "presentaciones": ["polvo"],
                "descripcion": "Creatina pura sin sabor"
            },
            {
                "nombre": "Creatine HCL 120 caps",
                "marca": "MuscleTech",
                "peso": "120 cápsulas",
                "precio": 65000,
                "stock": 7,
                "descuento": 8,
                "presentaciones": ["cápsulas"],
                "descripcion": "Creatina de absorción superior"
            },
            {
                "nombre": "Creatina Monohidrato 1kg",
                "marca": "Star Nutrition",
                "peso": "1kg",
                "precio": 85000,
                "stock": 6,
                "descuento": 20,
                "presentaciones": ["polvo"],
                "descripcion": "Creatina premium formato económico"
            }
        ]
    },
    "multivitaminico": {
        "categoria": "Multivitamínicos",
        "productos": [
            {
                "nombre": "Animal Pak 44 sobres",
                "marca": "Universal",
                "peso": "44 sobres",
                "precio": 95000,
                "stock": 4,
                "descuento": 5,
                "presentaciones": ["sobres"],
                "descripcion": "Multivitamínico completo para atletas"
            },
            {
                "nombre": "Opti-Men 90 tabs",
                "marca": "Optimum Nutrition",
                "peso": "90 tabletas",
                "precio": 55000,
                "stock": 10,
                "descuento": 10,
                "presentaciones": ["tabletas"],
                "descripcion": "Fórmula optimizada para hombres"
            },
            {
                "nombre": "Daily Formula 100 caps",
                "marca": "Star Nutrition",
                "peso": "100 cápsulas",
                "precio": 35000,
                "stock": 18,
                "descuento": 0,
                "presentaciones": ["cápsulas"],
                "descripcion": "Multivitamínico básico diario"
            }
        ]
    }
}

def consultar_precio_producto(producto):
    """
    Consulta los precios de productos específicos por categoría
    """
    producto = producto.lower()
    
    # Mapear diferentes formas de referirse a los productos
    mapeo_productos = {
        "proteina": ["proteina", "protein", "whey", "suero"],
        "creatina": ["creatina", "creatine"],
        "multivitaminico": ["multivitaminico", "vitaminas", "multivitaminas", "complejo"]
    }
    
    # Buscar la categoría
    categoria_encontrada = None
    for key, aliases in mapeo_productos.items():
        if any(alias in producto for alias in aliases):
            categoria_encontrada = key
            break
    
    if categoria_encontrada and categoria_encontrada in PRODUCTOS_DB:
        categoria = PRODUCTOS_DB[categoria_encontrada]
        productos = categoria["productos"]
        
        resultado = {
            "encontrado": True,
            "categoria": categoria["categoria"],
            "productos": []
        }
        
        for prod in productos:
            precio_final = prod["precio"]
            if prod["descuento"] > 0:
                precio_final = int(prod["precio"] * (1 - prod["descuento"]/100))
            
            resultado["productos"].append({
                "nombre": prod["nombre"],
                "precio_original": prod["precio"],
                "precio_final": precio_final,
                "descuento": prod["descuento"],
                "stock": prod["stock"]
            })
        
        return resultado
    
    return {"encontrado": False}

def disponibilidad_producto(producto):
    """
    Consulta disponibilidad de productos específicos
    """
    producto = producto.lower()
    
    mapeo_productos = {
        "proteina": ["proteina", "protein", "whey", "suero"],
        "creatina": ["creatina", "creatine"],
        "multivitaminico": ["multivitaminico", "vitaminas", "multivitaminas", "complejo"]
    }
    
    categoria_encontrada = None
    for key, aliases in mapeo_productos.items():
        if any(alias in producto for alias in aliases):
            categoria_encontrada = key
            break
    
    if categoria_encontrada and categoria_encontrada in PRODUCTOS_DB:
        categoria = PRODUCTOS_DB[categoria_encontrada]
        productos = categoria["productos"]
        
        resultado = {
            "encontrado": True,
            "categoria": categoria["categoria"],
            "productos": []
        }
        
        for prod in productos:
            estado = "✅ Disponible" if prod["stock"] > 0 else "❌ Agotado"
            resultado["productos"].append({
                "nombre": prod["nombre"],
                "stock": prod["stock"],
                "estado": estado
            })
        
        return resultado
    
    return {"encontrado": False}

def tiene_descuento(producto):
    """
    Consulta descuentos de productos específicos
    """
    producto = producto.lower()
    
    mapeo_productos = {
        "proteina": ["proteina", "protein", "whey", "suero"],
        "creatina": ["creatina", "creatine"],
        "multivitaminico": ["multivitaminico", "vitaminas", "multivitaminas", "complejo"]
    }
    
    categoria_encontrada = None
    for key, aliases in mapeo_productos.items():
        if any(alias in producto for alias in aliases):
            categoria_encontrada = key
            break
    
    if categoria_encontrada and categoria_encontrada in PRODUCTOS_DB:
        categoria = PRODUCTOS_DB[categoria_encontrada]
        productos = categoria["productos"]
        
        resultado = {
            "encontrado": True,
            "categoria": categoria["categoria"],
            "productos": []
        }
        
        for prod in productos:
            if prod["descuento"] > 0:
                precio_descuento = int(prod["precio"] * (1 - prod["descuento"]/100))
                resultado["productos"].append({
                    "nombre": prod["nombre"],
                    "tiene_descuento": True,
                    "porcentaje": prod["descuento"],
                    "precio_original": prod["precio"],
                    "precio_descuento": precio_descuento
                })
            else:
                resultado["productos"].append({
                    "nombre": prod["nombre"],
                    "tiene_descuento": False,
                    "precio_original": prod["precio"]
                })
        
        return resultado
    
    return {"encontrado": False}

def obtener_todos_productos():
    """
    Obtiene lista completa de todos los productos específicos
    """
    todos_productos = []
    
    for categoria_key, categoria_data in PRODUCTOS_DB.items():
        for prod in categoria_data["productos"]:
            precio_final = prod["precio"]
            if prod["descuento"] > 0:
                precio_final = int(prod["precio"] * (1 - prod["descuento"]/100))
            
            todos_productos.append({
                "categoria": categoria_data["categoria"],
                "nombre": prod["nombre"],
                "precio_original": prod["precio"],
                "precio_final": precio_final,
                "descuento": prod["descuento"],
                "stock": prod["stock"],
                "disponible": prod["stock"] > 0
            })
    
    return todos_productos

# AGREGAR esta función al final:
def buscar_producto_especifico(nombre_producto):
    """Busca un producto específico por nombre"""
    nombre_producto = nombre_producto.lower().strip()
    
    for categoria_key, categoria_data in PRODUCTOS_DB.items():
        for prod in categoria_data["productos"]:
            # Buscar por nombre
            if nombre_producto in prod["nombre"].lower():
                precio_final = prod["precio"]
                if prod["descuento"] > 0:
                    precio_final = int(prod["precio"] * (1 - prod["descuento"]/100))
                
                return {
                    "encontrado": True,
                    "nombre": prod["nombre"],
                    "precio_original": prod["precio"],
                    "precio_final": precio_final,
                    "descuento": prod["descuento"],
                    "stock": prod["stock"],
                    "disponible": prod["stock"] > 0
                }
    
    return {"encontrado": False}