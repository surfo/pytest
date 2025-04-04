## 200 OK (Solicitud Exitosa)

Este es el código de estado más común y significa que la solicitud se realizó correctamente.
El servidor ha procesado la solicitud y devuelve la información solicitada en el cuerpo de la respuesta.
Este código se utiliza para solicitudes GET, POST, PUT y DELETE exitosas.

## 500 Internal Server Error (Error Interno del Servidor)

Este código indica que el servidor encontró un error inesperado que le impidió completar la solicitud.
Generalmente, es un problema del lado del servidor y puede deberse a errores en el código, problemas de configuración o fallas en el servidor.
Los usuarios suelen ver este error cuando el servidor no puede proporcionar una respuesta más específica.

## 401 Unauthorized (No Autorizado)

Este código significa que el cliente no tiene las credenciales de autenticación válidas para acceder al recurso solicitado.
El servidor requiere autenticación y el cliente no la proporcionó o las credenciales proporcionadas son incorrectas.
A menudo, se muestra este error cuando se intenta acceder a una página o recurso protegido sin iniciar sesión o con credenciales incorrectas.

## 404 Not Found (No Encontrado)

Este código indica que el servidor no pudo encontrar el recurso solicitado.
Esto puede deberse a que la URL es incorrecta, el recurso se ha eliminado o el servidor no puede encontrarlo.
Es uno de los códigos de error más comunes y se muestra cuando se intenta acceder a una página que no existe.

## 400 Bad Request (Solicitud Incorrecta)

Este código significa que el servidor no pudo entender la solicitud debido a una sintaxis incorrecta o datos inválidos en la solicitud.
Esto puede deberse a errores en los parámetros de la solicitud, datos faltantes o formatos incorrectos.
Indica que el cliente debe corregir la solicitud antes de enviarla nuevamente.

## 422 Unprocessable Entity (Entidad No Procesable)

Este código indica que el servidor entiende la solicitud, pero no puede procesarla debido a errores semánticos en los datos de la solicitud.
A menudo, se utiliza para indicar errores de validación en los datos enviados en la solicitud.
Este codigo es utilizado cuando la sintaxis de la petición es correcta, pero la semántica de la peticion no.