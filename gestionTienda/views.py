from django.shortcuts import render
from gestionTienda.models import Clientes, Pedidos, Productos
from django.http import HttpResponse, HttpRequest
from pymongo import MongoClient
from bson.objectid import ObjectId
# Create your views here.
from django.conf import settings

def gestion_tienda(request):
    try:
        client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        databasem = client[settings.MONGO_BD]
        collection = databasem[settings.MONGO_COLLECTION]

        documents = list(collection.find()) 
    except Exception as ex:
        return HttpResponse("Error durante la conexión")
    finally:
        client.close()
    
    return render(request, "gestion_tienda.html", {"registros": documents})



def agregar_cliente(request):
    nombre = request.GET["nombre_cliente"]
    dni = request.GET["dni_cliente"]
    email = request.GET["email_cliente"]
    telefono = request.GET["telefono_cliente"]
    cliente = Clientes(nombre=nombre, dni=dni, email=email, telefono=telefono)
    cliente.save()
    return render(request, "agregar/cliente_agregado.html", {"cliente":cliente, "titulo": "Se ha agregado el cliente"})

def agregar_pedido(request):
    dni = request.GET["dni_pedido"]
    id_producto = request.GET["id_producto_pedido"]
    cantidad = request.GET["cantidad_pedido"]

    pedido = Pedidos(dni=dni, id_producto=id_producto, cantidad=cantidad)
    pedido.save()
    return render(request, "agregar/pedido_agregado.html", {"pedido":pedido,"titulo":"Se ha agregado el pedido"})

def agregar_producto(request):
    id_producto = request.GET["id_producto"]
    nombre = request.GET["nombre_producto"]
    precio = request.GET["precio_producto"]
    categoria = request.GET["categoria_producto"]
    producto = Productos(id_producto=id_producto, nombre=nombre, precio=precio, categoria=categoria)
    producto.save()
    return render(request, "agregar/producto_agregado.html", {"producto":producto,"titulo":"Se ha agregado el producto"})


def modificar_cliente(request):
    dni_cliente = request.GET["input_cliente"]
    try: 
        cliente = Clientes.objects.get(dni=dni_cliente) 
    except Clientes.DoesNotExist: 
        return HttpResponse("No existe un cliente con dni: %r" %request.GET["input_cliente"])
    return render(request, "modificar/modificar_cliente.html",{"cliente":cliente})

def cliente_modificado(request):
    dni_previo = request.GET["clave_previa"]
    dni_nuevo = request.GET["dni_cliente"]
    
    cliente = Clientes.objects.get(dni=dni_previo) 
    if (dni_previo == dni_nuevo):
        cliente.email = request.GET["email_cliente"]
        cliente.telefono = request.GET["telefono_cliente"]
        cliente.nombre = request.GET["nombre_cliente"]
        cliente.save()
        return render(request, "agregar/cliente_agregado.html",{"cliente":cliente})
    try:#Si quiere cambiar el dni entonces elimino el registro y creo uno nuevo
        cliente = Clientes.objects.get(dni=dni_nuevo)
        msg = "Error: existe un cliente con el mismo dni a cambiar: %r" %request.GET["dni_cliente"]
        return render(request, "error_msg.html",{"error_msg":msg})
    
    except Clientes.DoesNotExist: #si no tengo un registro con el nuevo dni entonces creo el nuevo registro
        cliente.delete()
        cliente = Clientes(dni = dni_nuevo, nombre=request.GET["nombre_cliente"], email=request.GET["email_cliente"], telefono=request.GET["telefono_cliente"])
        cliente.save()
            
    
    return render(request, "agregar/cliente_agregado.html",{"cliente":cliente, "titulo":"Se ha modificado el Cliente"})

def clientes_en_tablas(request):
    clientes = Clientes.objects.all()[:20]
    return render(request, "ver_tablas/clientes_en_tablas.html", {"clientes": clientes})

def pedidos_en_tablas(request):
    pedidos = Pedidos.objects.all()[:20]
    return render(request, "ver_tablas/pedidos_en_tablas.html", {"pedidos": pedidos})

def productos_en_tablas(request):
    productos = Productos.objects.all()[:20]
    return render(request, "ver_tablas/productos_en_tablas.html", {"productos": productos})

def modificar_pedido(request):
    id_pedido = request.GET["input_pedido"]
    try: 
        pedido = Pedidos.objects.get(id_pedido=id_pedido) 
        
    except Pedidos.DoesNotExist: 
        return HttpResponse("No existe el  pedido con id: %r" %request.GET["input_pedido"])
    try:
        cliente = Clientes.objects.get(dni=pedido.dni)
    except Clientes.DoesNotExist: 
        cliente = Clientes(dni=-1,nombre="eliminado",email=".", telefono=".")
    try:
        producto = Productos.objects.get(id_producto=pedido.id_producto) 
    except Producto.DoesNotExist: 
        producto = Productos(id_producto = -1, nombre="eliminado", precio=-1, categoria=".")
    return render(request, "modificar/pedidos_completo.html",{"pedido":pedido,"producto":producto,"cliente":cliente})

def pedido_modificado(request):
    id_previo = request.GET["clave_previa"]
    id_nuevo = request.GET["id_pedido"]
    
    dni = request.GET["dni_pedido"]
    id_producto = request.GET["id_producto_pedido"]
    cantidad = request.GET["cantidad_pedido"]

    
    if (id_previo == id_nuevo):
        pedido = Pedidos.objects.get(id_producto=id_previo) 
        pedido.dni = dni
        pedido.id_producto = id_producto
        pedido.cantidad = cantidad
        
        pedido.save()
        return render(request, "agregar/pedido_agregado.html",{"pedido":pedido, "titulo": "Se ha modificado el titulo"})
    try:#Si quiere cambiar el dni entonces elimino el registro y creo uno nuevo
        pedido = Pedidos.objects.get(dni=id_nuevo)
        msg = "Error: existe un pedido con el mismo dni a cambiar: %r" %request.GET["id_pedido"]
        return render(request, "error_msg.html",{"error_msg":msg})
    
    except Pedidos.DoesNotExist: #si no tengo un registro con el nuevo id entonces creo el nuevo registro pero elimino el anterior
        pedido = Pedidos.objects.get(id_producto=id_previo) 
        pedido.delete()
        pedido = Pedidos(dni=dni, id_producto=id_producto, cantidad=cantidad)
        pedido.save()
            
    
    return render(request, "agregar/pedido_agregado.html",{"pedido":pedido, "titulo": "Se ha modificado el Pedido"})

def modificar_producto(request):
    id_producto = request.GET["input_producto"]
    try: 
        producto = Productos.objects.get(id_producto=id_producto) 
    except Productos.DoesNotExist: 
        return HttpResponse("No existe el producto con id: %r" %request.GET["input_producto"])
    return render(request, "modificar/modificar_producto.html",{"producto":producto})

def producto_modificado(request):
    id_previo = request.GET["clave_previa"]
    id_nuevo = request.GET["id_producto"]
    
    nombre = request.GET["nombre_producto"]
    precio = request.GET["precio_producto"]
    categoria = request.GET["categoria_producto"]

    
    if (id_previo == id_nuevo):
        producto = Productos.objects.get(id_producto=id_previo) 
        producto.nombre = nombre
        producto.precio = precio
        producto.categoria = categoria
        
        producto.save()
        return render(request, "agregar/producto_agregado.html",{"producto":producto, "titulo": "Se ha modificado el Producto"})
    try:#Si quiere cambiar el dni entonces elimino el registro y creo uno nuevo
        producto = Productos.objects.get(id_producto=id_nuevo)
        msg = "Error: existe un producto con el mismo dni a cambiar: %r" %request.GET["id_producto"]
        return render(request, "error_msg.html",{"error_msg":msg})
    
    except Productos.DoesNotExist: #si no tengo un registro con el nuevo id entonces creo el nuevo registro pero elimino el anterior
        producto = Productos.objects.get(id_producto=id_previo) 
        producto.delete()
        producto = Productos(id_producto=id_nuevo, nombre=nombre, precio=precio, categoria=categoria)
        producto.save()
            
    return render(request, "agregar/producto_agregado.html",{"producto":producto, "titulo": "Se ha modificado el Producto"})


def eliminar_cliente(request):
    dni_previo = request.GET["clave_previa"]
    cliente = Clientes.objects.get(dni=dni_previo) 
    cliente.delete()
    msg = "Se ha eliminado el cliente con dni: %r" %dni_previo
    return render(request, "notificacion_msg.html",{"notificacion_msg":msg})


def eliminar_pedido(request):
    id_previo = request.GET["clave_previa"]
    pedido = Pedidos.objects.get(id_pedido=id_previo) 
    pedido.delete()
    msg = "Se ha eliminado el pedido de id: %r" %id_previo
    return render(request, "notificacion_msg.html",{"notificacion_msg":msg})

def eliminar_producto(request):
    id_previo = request.GET["clave_previa"]
    producto = Productos.objects.get(id_producto=id_previo) 
    producto.delete()
    msg = "Se ha eliminado el producto  de id: %r" %id_previo
    return render(request, "notificacion_msg.html",{"notificacion_msg":msg})


def gestion_mongodb(request):
    try:
        client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        databasem = client[settings.MONGO_BD]
        collection = databasem[settings.MONGO_COLLECTION]

        documents = list(collection.find()) 
    except Exception as ex:
        return HttpResponse("Error durante la conexión")
    finally:
        client.close()
    
    return render(request, "no_relacional.html", {"registros": documents})

def agregar_producto_nosql(request):
  

    client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    databasem = client[settings.MONGO_BD]
    collection = databasem[settings.MONGO_COLLECTION]

    descripcion = request.GET.get("descripcion_producto_nosql", "")
    stock = request.GET.get("stock_producto_nosql", "")
    categorias = request.GET.get("categorias_producto_nosql", "")
    imagen1 = request.GET.get("imagen1_producto_nosql", "")
    descripcion1 = request.GET.get("descripcion1img_producto_nosql", "")
    imagen2 = request.GET.get("imagen2_producto_nosql", "")
    descripcion2 = request.GET.get("descripcion2img_producto_nosql", "")
    if not categorias:
        categorias = []
    else:
        categorias = categorias.split(",")
    # Crear un nuevo registro
    nuevo_producto = {
        "nombre": request.GET["nombre_producto_nosql"],
        "precio": request.GET["precio_producto_nosql"],
        "marca": request.GET["marca_producto_nosql"],
        "descripcion": descripcion,
        "stock": stock,
        "categorias": categorias,
        "imagenes": [
            {"url": imagen1, "descripcion": descripcion1},
            {"url": imagen2, "descripcion": descripcion2}
        ]
    }

    # Insertar el registro en la colección
    resultado = collection.insert_one(nuevo_producto)

    # Mostrar el ID del nuevo registro

    # Cerrar la conexión
    client.close()
    msg = "Se modifico el producto: %r" %request.GET["nombre_producto_nosql"]
    return render(request,"notificacion_msg.html", {"notificacion_msg":msg})

def buscar_nosql(request):
    client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    databasem = client[settings.MONGO_BD]
    collection = databasem[settings.MONGO_COLLECTION]

    clave = request.GET["atributo_nosql"]
    valor = request.GET["buscador_nosql"]
    if( clave != "categoria"):

        #registros = collection.find({clave: valor})
        registros = collection.find({clave: {"$regex": valor, "$options": "i"}})
    else:
        #registros = collection.find({"categorias": {"$in": [valor]}})
        regex = f".*{valor}.*" 
        registros = collection.find({"categorias": {"$regex": regex, "$options": "i"}}) 
    
    return render(request, "nosql/coincidencias_nosql.html", {"registros":registros})


def modificar_nosql(request):
    client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    databasem = client[settings.MONGO_BD]
    collection = databasem[settings.MONGO_COLLECTION]

    # Criterio de búsqueda usando _id
    id = request.GET["_id"]
    criterio = {"_id": ObjectId(id)}

    # Nuevos valores
    nombre = request.GET.get("nombre", "").strip()
    descripcion = request.GET.get("descripcion", "").strip()
    marca = request.GET.get("marca", "").strip()
    
    precio = request.GET.get("precio", "").strip()
    stock = request.GET.get("stock", "").strip()
    categorias = request.GET.get("categorias", "").strip()
    imagenes = request.GET.get("imagenes", "").strip()
    nuevos_valores = {"$set": {"nombre": nombre,"descripcion":descripcion, "marca": marca, "precio": precio, "stock": stock, "categorias":categorias, "imagenes":imagenes}}

    # Actualizar el documento
    resultado = collection.update_one(criterio, nuevos_valores)
    client.close()
    if resultado.matched_count > 0:
        msg = "Se modifico el producto: %r" %request.GET["nombre"]
        return render(request,"notificacion_msg.html", {"notificacion_msg":msg})
    else:
        return HttpResponse("no se encontro con :%r" %id)

    

def eliminar_nosql(request):
    client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    databasem = client[settings.MONGO_BD]
    collection = databasem[settings.MONGO_COLLECTION]

    id = request.GET["_id"]
    criterio = {"_id": ObjectId(id)}
    resultado = collection.delete_one(criterio)
    client.close()
    if resultado.deleted_count > 0: 
        return HttpResponse("Se elimino el producto: %r" %request.GET["nombre"])
    else: 
        return HttpResponse("no se encontro con :%r" %id)
    