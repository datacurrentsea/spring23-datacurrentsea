#Run after az login and g
TAG=$(git rev-parse --short HEAD)

sed "s/\[TAG\]/${TAG}/g" .k8s/overlays/prod/patch-deployment-project_copy.yaml > .k8s/overlays/prod/patch-deployment-project.yaml

IMAGE_NAME=project
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_PREFIX=giomola
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}"

cd mlapi/
docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} .
docker tag ${IMAGE_NAME} ${IMAGE_FQDN}:${TAG}
docker push ${IMAGE_FQDN}:${TAG}
docker pull ${IMAGE_FQDN}:${TAG}