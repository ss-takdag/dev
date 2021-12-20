1. Set the required environment variables in the dockerfile.


2. Build and push container to ecr
    ./docker_push_ecr.sh -b yes -tTAG -rRELEASE -iNAME_OF_IMAGE -aECR_URI

    ex. ./docker_push_ecr.sh -b yes -tbuild1 -r1.0 -itest_image -a 1234.dkr.ecr.us-east-1.amazonaws.com

3. update stack.yml and create stack. Or update stack to switch lambda function to new release
