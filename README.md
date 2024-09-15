# Cargo Express App

Esta aplicación se encarga de registrar pedidos en tiempo real hechos por los diferentes repartidores de la empresa cargo-express utilizando 
como base [Django](https://www.djangoproject.com/), ya que esta proporciona diversas herramientas que facilitan el desarrollo de aplicaciones 
web complejas. Django porque permite escribir código más limpio y mantenible, facilitando la creación de modelos de datos y su interacción 
con la base de datos, lo que a su vez me permite enfocarme en la lógica de negocio sin preocuparme por los detalles de implementación de la 
base de datos. Además, Django proporciona protección contra ataques comunes como [SQL Injection](https://developer.mozilla.org/en-US/docs/Glossary/SQL_Injection), 
[Cross-Site Scripting (XSS)](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting) y [Cross-Site Request Forgery (CSRF)](https://developer.mozilla.org/en-US/docs/Glossary/CSRF) y 
también permite hacer el hashing de contraseñas de forma segura, lo que da tranquilidad en cuanto a la seguridad de la aplicación.

Por otro lado, para garantizar la escalabilidad y despliegue de la aplicación, utilizo Docker, una plataforma de contenerización que me permite crear 
contenedores que incluyen la aplicación y sus dependencias. Esto me permite desplegar la aplicación de manera rápida y segura en diferentes entornos.

Además, la aplicación utiliza PostgreSQL como sistema de gestión de base de datos, lo que me permite almacenar y recuperar datos de manera eficiente y segura.

Adicionalmente esta aplicación cuenta con un panel para monitorear los pedidos en tiempo cercano al real en donde podremos ver el producto mas vendido y
sus cantidades, el repartidor que ha entregado mas pedidos, una grafica de barras que muestra el total de ventas por producto y tambien podremos ver los 
ingresos totales por producto esto gracias a una tecnología llamada [WebSockets](https://developer.mozilla.org/es/docs/Web/API/WebSockets_API) para actualizar la información 
en tiempo real, esto se logra combinando Django y Redis (Base de datos en memoria que se utiliza para almacenar datos de manera muy rápida)

## Requisitos
- Tener instalado [Docker desktop](https://www.docker.com/products/docker-desktop/)
- Tener acceso a una terminal o línea de comandos (como Terminal en macOS o Linux, o Command Prompt en Windows)

## Pasos para Ejecutar la Aplicación

1. **Clonar el Repositorio**:
   ```sh
   git clone https://github.com/camiloV32/cargo-express.git
   cd <RUTA_DEL_PROYECTO>
   ```
2. **Construir y levantar el contenedor**:
   ```sh
   docker-compose up --build
   ```
3. **Acceder a la Aplicación**:
   - La aplicación web estará disponible en `http://localhost:8000`
## Modelos
![Modelo](https://raw.githubusercontent.com/camiloV32/cargo-express/master/.github/DiagramaBD.png)

**Delivery**
| Campo | Tipo de Dato | Descripcion |
| --- | --- | --- |
| id | Integer | Identificador unico del envio |
| user_id | ForeignKey (User) | Identificador del repartidor |

**Order**
| Campo | Tipo de Dato | Descripcion |
| --- | --- | --- |
| order_code | UUIDField | Codigo unico del pedido |
| delivery | ForeignKey (Delivery) | Pedido asociado al repartidor |
| timestamp | DateTimeField | Fecha y hora del pedido |

**OrderProduct**
| Campo | Tipo de Dato | Descripcion |
| --- | --- | --- |
| order | ForeignKey (Order) | Pedido asociado al producto |
| product | ForeignKey (Product) | Producto asociado al pedido |
| quantity | PositiveIntegerField | Cantidad del producto en el pedido |

**Product**
| Campo | Tipo de Dato | Descripcion |
| --- | --- | --- |
| id | CharField (max_length=20) | Identificador unico del producto |
| name | CharField (max_length=40) | Nombre del producto |
| price | DecimalField (decimal_places=3, max_digits=15) | Precio del producto |

**Role**
| Campo | Tipo de Dato | Descripcion |
| --- | --- | --- |
| name | CharField (max_length=20) | Nombre del rol |

**User**
| Campo | Tipo de Dato | Descripcion |
| --- | --- | --- |
| name | CharField (max_length=20) | Nombre del usuario |
| email | EmailField | Correo electronico del usuario |
| password | CharField (max_length=100) | Contraseña del usuario |
| role_id | ForeignKey (Role) | Rol asociado al usuario |

## Arquitectura del proyecto
Este proyecto se encuentra construido con django y cuenta con 2 aplicaciones, la primera para registrar los pedidos y verificar que el repartidor esta registrado en la base de datos,
la segunda contiene un login que de acceso a un panel en el que podemos observar diferentes metricas de los pedidos en tiempo cercano al real mediante WebSockets, que permite una comunicación 
bidireccional entre el servidor y el cliente, y Redis como base de datos en memoria para almacenar datos de manera rápida y eficiente. De esta manera, el dashboard puede mostrar información actualizada instantáneamente.

## Rutas

**Endpoint:** `/api/obtener_token_delivery/`

**Método:** `POST`

**Encabezado de la petición:**
* **Body:** Debe contener los siguientes campos:
	+ **IdRepartidor:** Un entero (`int`) que representa el ID del repartidor.
	+ **Nombre:** Una cadena de texto (`string`) que representa el nombre del repartidor.

**Respuesta del servidor:**
* **Código de estado:** `200 OK` si la petición es exitosa.
* **Cuerpo de la respuesta:** Un objeto JSON con los siguientes campos:
	+ **token:** Una cadena de texto (`string`) que representa el token de autenticación.
	+ **message:** Una cadena de texto (`string`) con el mensaje "Ok" que indica que la petición fue exitosa.

***

**Endpoint:** `/api/registrar_pedido_entregado/`

**Método:** `POST`

**Encabezado de la petición:**
* **Headers:** Debe contener el siguiente campo:
	+ **Authorization:** Una cadena de texto (`string`) que representa el token de autenticación obtenido en `/api/obtener_token_delivery/`
* **Body:** Debe contener los siguientes campos:
	+ **pedido_id:** Una cadena de texto (`string`) que representa el ID del pedido.
	+ **repartidor:** Un objeto con los siguientes campos:
		- **IdRepartidor:** Un entero (`int`) que representa el ID del repartidor.
		- **Nombre:** Una cadena de texto (`string`) que representa el nombre del repartidor.
	+ **productos:** Un arreglo de objetos con los siguientes campos:
		- **IdProducto:** Una cadena de texto (`string`) que representa el ID del producto.
		- **producto:** Una cadena de texto (`string`) que representa el nombre del producto.
		- **precio:** Un número flotante (`float`) que representa el precio del producto.
	+ **timestamp:** Una cadena de texto (`string`) que representa la marca de tiempo.

**Respuesta del servidor:**
* **Código de estado:** `201 Created` si la petición es exitosa.
* **Cuerpo de la respuesta:** Un objeto JSON con los siguientes campos:
	+ **message:** Una cadena de texto (`string`) con el mensaje "Create".
	+ **id_orden:** Una cadena de texto (`string`) que representa el ID de la orden.
	+ **products:** Un arreglo de objetos que representan los productos creados.

***

**Endpoint:** `/dashboard/login/`


#### POST

**Encabezado de la petición:**
* **Body:** Debe contener los siguientes campos:
	+ **username:** Una cadena de texto (`string`) que representa el correo electrónico del usuario.
	+ **password:** Una cadena de texto (`string`) que representa la contraseña del usuario.

**Respuesta del servidor:**
* **Cuerpo de la respuesta:** Redirige al usuario a la página de administración (`/dashboard/admin/`).


#### GET

**Respuesta del servidor:**
* **Código de estado:** `200 OK`
* **Cuerpo de la respuesta:** Renderiza la página de login (`dashboard/login`).

***

**Endpoint:** `/dashboard/admin`

**Método:** `POST`

**Requisitos de autenticación:**
* El usuario debe estar autenticado.

**Parámetros de la petición:**
* Ninguno.

**Respuesta del servidor:**
* **Cuerpo de la respuesta:** Renderiza la página de administración (`dashboard/admin`) con el correo electrónico del usuario autenticado.

## Preguntas teóricas
### ¿Qué recomendaciones le darías para que pueda garantizar su operación?
Estar monitoreando constantemente los servicios cloud en los que se va a desplegar esta aplicación ya que si hay mucha demanda de recursos es posible que el servidor se vea afectado en rendimiento e incluso podria provocar errores por no ser capaz de procesar las solicitudes, tambien se recomiendaquew se configure el servidor para que gradualmente responda a la demanda de recursos (Auto Scaling)

### ¿La solución planteada se encuentra en la capacidad de responder la demanda durante los próximos dos años?
Con un monitoreo de los servicios desplegados en la nube para este desarrollo (Amazon ElastiCache, RDS y Amazon Elastic Beanstalk) y siguiendo las recomendaciones anteriores se encuentra en la capacidad de responder a la demanda sin embargo seria lo ideal realizar diferentes pruebas de la solución como lo son pruebas de estres para resolver posibles problemas que se producción o ver como se comportan los diferentes servicios frente a ciertos escenarios. 
