# Proyecto Inventario CRUD - Flask + PostgreSQL + Kubernetes

Aplicación web para crear, listar, editar y eliminar productos. Incluye contenedor Docker y manifiestos Kubernetes.

## 1. Ejecutar localmente con Docker Compose

Requisito: Docker Desktop con Docker Compose.

```bash
docker compose up --build
```

Abrir http://localhost:5000

Para detener:
```bash
docker compose down
```

Los datos locales se guardan en el volumen `postgres_data`. Para borrar también la base local:
```bash
docker compose down -v
```

## 2. Construir y publicar imagen

Crea una cuenta en Docker Hub, inicia sesión y reemplaza `TU_USUARIO_DOCKERHUB`:

```bash
docker build -t TU_USUARIO_DOCKERHUB/inventario-web:1.0 .
docker login
docker push TU_USUARIO_DOCKERHUB/inventario-web:1.0
```

Edita `kubernetes/deployment.yaml` y coloca tu imagen publicada.

## 3. Desplegar en Kubernetes

Necesitas un clúster Kubernetes, un Ingress Controller (por ejemplo NGINX), metrics-server y una StorageClass que aprovisione volúmenes persistentes.

Aplica los manifiestos:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/config-secret.yaml
kubectl apply -f kubernetes/service-db.yaml
kubectl apply -f kubernetes/statefulset-db.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service-web.yaml
kubectl apply -f kubernetes/hpa.yaml
kubectl apply -f kubernetes/ingress.yaml
```

**Antes de aplicar:** cambia las claves del archivo `config-secret.yaml` y la imagen del Deployment. No uses las claves de ejemplo en un entorno real.

Ver estado:
```bash
kubectl get pods -n inventario
kubectl get deployment,statefulset,svc,hpa,ingress -n inventario
kubectl describe hpa inventario-web-hpa -n inventario
```

El HPA usa memoria (no CPU), con mínimo 2 y máximo 5 réplicas. Requiere metrics-server y `resources.requests.memory`.

## 4. Ingress local

Con un clúster local, configura la resolución de `inventario.local` hacia la IP de entrada de tu Ingress Controller. La IP y el método dependen de Minikube, Docker Desktop o el clúster que uses.

## Componentes entregados

- Flask con interfaz HTML/CSS y CRUD de productos.
- PostgreSQL.
- Dockerfile y Docker Compose para prueba local.
- Deployment web (2 réplicas iniciales).
- Service tipo LoadBalancer.
- HPA por memoria (2 a 5 réplicas).
- StatefulSet PostgreSQL (1 réplica) con PVC de 2Gi.
- Ingress HTTP.

## Nota académica

El Service `LoadBalancer` y el Ingress están incluidos para cumplir el esquema solicitado. En algunos clústeres locales, el tipo LoadBalancer necesita soporte adicional (por ejemplo, MetalLB o el mecanismo propio del entorno). Para tráfico HTTP, el Ingress enruta hacia el Service.
