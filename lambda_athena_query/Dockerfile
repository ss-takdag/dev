FROM public.ecr.aws/lambda/python:3.8
ENV TZ="America/Los_Angeles"

# Install the function's dependencies using file requirements.txt
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}
COPY athena_from_s3.py ${LAMBDA_TASK_ROOT}
COPY email_handler.py ${LAMBDA_TASK_ROOT}
COPY google_sheets_handler.py ${LAMDBA_TASK_ROOT}
COPY s3_handler.py ${LAMBDA_TASK_ROOT}
COPY query.txt ${LAMBDA_TASK_ROOT}
COPY secret_manager.py ${LAMBDA_TASK_ROOT}
COPY sns_handler.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]

#REQUIRED ENVIRONEMT VARIABLES
ENV DESTINATION_BUCKET="dev-ss-s3notify2"
ENV BUCKET_PATH="temp/athena/output"
ENV ATHENA_DATABASE="default"
ENV AWS_REGION="us-east-1"
ENV EMAIL_FROM_ADDRESS="ss.dev.aws@gmail.com"
ENV EMAIL_RECIPIENTS="tedd.akdag@sendsafely.com"
ENV GOOGLE_API_ACCOUNT="ytestsa@circular-nova-334605.iam.gserviceaccount.com"
ENV APPEND_GOOGLE_SHEET_KEY="14cmYlIOkP892KjOFNyrz0cDYH-VzT1UMVk35ygxOFNE"
