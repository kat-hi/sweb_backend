## Frontend
- **app-deployment** | running replicas on k8s
- **app-service** | providing stable IP-address for all pods inside the cluster
- **app-ingress** | exposing the app via app.stark-wie-ein-baum.de

## Api
- **api-config.yaml** # configMap with environment variables and secrets
- **api-deployment.yaml** # running backend replicas on k8s
- **api-service.yaml** # providing stable IP-address for all pods inside the cluster
- **api-ingress.yaml** # making the api accessible

## Admin
- **admin-api-ingress.yaml** # exposing the admin interface via admin.stark-wie-ein-baum.de

## Database
- **mysql-deployment.yaml** # running mysql-instance on k8s
- **mysql-service.yaml** # providing stable IP-address inside the cluster
- **mysql-pvc.yaml** # using persistant storage. volume is mounted inside the mysql-pod
