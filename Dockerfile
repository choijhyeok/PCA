FROM python:3.7.5-slim

# Installing packages
#RUN apt update
RUN pip3 install --no-cache scikit-learn numpy boto3 botocore pandas joblib flask

# Defining working directory and adding source code
WORKDIR /usr/src/app

# in case that you want to store some in here...
# but it'd better store files in /tmp/
RUN mkdir -p /usr/src/app/tmp_files
RUN chmod 755 /usr/src/app/tmp_files

COPY bootstrap.sh ./
COPY pca-image ./pca-image

RUN chmod 755 /usr/src/app/bootstrap.sh
RUN chmod +x /usr/src/app/bootstrap.sh

# Start app
EXPOSE 50000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
