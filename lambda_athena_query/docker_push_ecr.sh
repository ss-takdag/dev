#!/bin/bash
BUILDDIR="."

while getopts :b:t:d:r:i:a: option; do
        case ${option} in
        b) BUILD=${OPTARG};;
        t) TAG=${OPTARG};;
        d) BUILDDIR=${OPTARG};;
        r) RELEASE=${OPTARG};;
        i) ECR_IMAGE=${OPTARG};;
        a) ECR_ADDRESS=${OPTARG};;
        ?) printf "Usage: -b BUILD OR NOT -t tag -d builddir -r relase -i image -a ecr address"
        esac
done

echo ${TAG}:${RELEASE} ${BUILDDIR}

# aws cloudformation delete-stack --stack-name iam1
#
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_ADDRESS}


if [[ -n ${BUILD} ]]; then
  echo "Building Docker Image"
  echo "executing docker build -t ${TAG}:${RELEASE} ${BUILDDIR}"
  docker build -t ${TAG}:${RELEASE} ${BUILDDIR}
fi
#
echo "tagging image"
docker tag ${TAG}:${RELEASE} ${ECR_ADDRESS}/${ECR_IMAGE}:${RELEASE}

echo "pushing image to ${ECR_ADDRESS}"
docker push ${ECR_ADDRESS}/${ECR_IMAGE}:${RELEASE}

aws ecr describe-images --repository-name ${ECR_IMAGE} --image-ids imageTag=${RELEASE}
