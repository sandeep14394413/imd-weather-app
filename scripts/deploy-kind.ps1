param(
    [string]$ClusterName = "kind",
    [string]$Namespace = "imd-weather",
    [string]$JwtSecret = "change-this-secret-before-production"
)

$ErrorActionPreference = "Stop"
$ImageTag = Get-Date -Format "yyyyMMddHHmmss"

docker build -f Dockerfile.api -t imd-weather-api:$ImageTag .
docker build -f Dockerfile.ui -t imd-weather-ui:$ImageTag .

kind load docker-image imd-weather-api:$ImageTag --name $ClusterName
kind load docker-image imd-weather-ui:$ImageTag --name $ClusterName

kubectl apply -f k8s/00-namespace.yaml
kubectl -n $Namespace create secret generic imd-weather-app-secret `
    --from-literal=jwt-secret=$JwtSecret `
    --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f k8s/10-api.yaml
kubectl apply -f k8s/20-ui.yaml
kubectl -n $Namespace set image deployment/imd-weather-api api=imd-weather-api:$ImageTag
kubectl -n $Namespace set image deployment/imd-weather-ui ui=imd-weather-ui:$ImageTag
kubectl -n $Namespace rollout status deployment/imd-weather-api --timeout=180s
kubectl -n $Namespace rollout status deployment/imd-weather-ui --timeout=180s

Write-Host "Port forward UI with:"
Write-Host "kubectl -n $Namespace port-forward svc/imd-weather-ui 8501:8501"
