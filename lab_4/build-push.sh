TAG=$(git rev-parse --short HEAD)
sed "s/\[TAG\]/${TAG}/g" .k8s/overlays/prod/patch-deployment-lab4_copy.yaml > .k8s/overlays/prod/patch-deployment-lab4.yaml

IMAGE_NAME=lab4
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_PREFIX=giomola
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}"



echo "docker tag ${IMAGE_NAME} ${IMAGE_FQDN}:${TAG}"
echo "docker push ${IMAGE_FQDN}:${TAG}"
echo "docker pull ${IMAGE_FQDN}:${TAG}"