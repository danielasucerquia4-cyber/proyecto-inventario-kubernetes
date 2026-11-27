# Sistema de Inventario CRUD con Kubernetes

## Descripción del proyecto

Aplicación web desarrollada con Flask y PostgreSQL que permite gestionar un inventario de productos mediante operaciones CRUD (crear, consultar, actualizar y eliminar).

El proyecto utiliza Docker para la contenerización y Kubernetes para la orquestación y administración de los servicios.

## Tecnologías utilizadas

- Python y Flask.
- PostgreSQL.
- HTML y CSS.
- Docker y Docker Compose.
- Kubernetes.
- Minikube.
- NGINX Ingress Controller.
- Horizontal Pod Autoscaler (HPA).

## Funcionalidades

- Registrar productos.
- Consultar productos almacenados.
- Editar productos.
- Eliminar productos.
- Almacenar información en PostgreSQL.

## Arquitectura de Kubernetes

El proyecto incluye los siguientes recursos:

| Recurso | Configuración |
|---|---|
| Namespace | inventario |
| Deployment web | 2 réplicas iniciales |
| Límite de réplicas | Mínimo 2 y máximo 5 |
| Service web | LoadBalancer |
| HPA | Escalamiento por memoria al 70 % |
| StatefulSet | PostgreSQL con 1 réplica |
| Persistent Volume Claim | Almacenamiento persistente de 2 GiB |
| Service de base de datos | ClusterIP headless |
| Ingress | NGINX, dominio inventario.local |

El HPA utiliza el consumo de memoria para ajustar automáticamente la cantidad de réplicas del Deployment web, dentro del rango configurado.

## Estructura del proyecto

```text
proyecto-inventario/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   └── style.css
│   └── templates/
│       └── index.html
├── kubernetes/
│   ├── namespace.yaml
│   ├── config-secret.example.yaml
│   ├── deployment.yaml
│   ├── service-web.yaml
│   ├── service-db.yaml
│   ├── statefulset-db.yaml
│   ├── hpa.yaml
│   └── ingress.yaml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Ejecución local con Docker Compose

Ejecutar:

```bash
docker compose up --build
```

Abrir en el navegador:

```text
http://localhost:5000
```

Para detener los contenedores:

```bash
docker compose down
```

## Despliegue en Kubernetes con Minikube

Iniciar Minikube:

```bash
minikube start
```

Habilitar los complementos necesarios:

```bash
minikube addons enable ingress
minikube addons enable metrics-server
```

Crear el archivo de configuración de secretos a partir de la plantilla:

```bash
cp kubernetes/config-secret.example.yaml kubernetes/config-secret.yaml
```

Editar el archivo y establecer las credenciales correspondientes.

Aplicar los manifiestos:

```bash
minikube kubectl -- apply -f kubernetes/namespace.yaml
minikube kubectl -- apply -f kubernetes/config-secret.yaml
minikube kubectl -- apply -f kubernetes/service-db.yaml
minikube kubectl -- apply -f kubernetes/statefulset-db.yaml
minikube kubectl -- apply -f kubernetes/deployment.yaml
minikube kubectl -- apply -f kubernetes/service-web.yaml
minikube kubectl -- apply -f kubernetes/hpa.yaml
minikube kubectl -- apply -f kubernetes/ingress.yaml
```

Para consultar los recursos:

```bash
minikube kubectl -- get pods -n inventario
minikube kubectl -- get services -n inventario
minikube kubectl -- get deployments -n inventario
minikube kubectl -- get statefulsets -n inventario
minikube kubectl -- get hpa -n inventario
minikube kubectl -- get pvc -n inventario
minikube kubectl -- get ingress -n inventario
```

## Acceso a la aplicación

La aplicación se encuentra disponible mediante el dominio local:

```text
http://inventario.local
```

Este dominio requiere configurar la resolución local hacia la dirección IP del Ingress de Minikube.

## Imagen Docker

Imagen publicada en Docker Hub:

```text
danielasc5/inventario-web:1.0
```

## Seguridad

El archivo `kubernetes/config-secret.yaml` contiene credenciales de configuración y no debe publicarse en el repositorio.

Se incluye `kubernetes/config-secret.example.yaml` como plantilla para configurar las credenciales propias.


