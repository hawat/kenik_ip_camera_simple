# Use the official Python base image
FROM python:3.9-slim
LABEL authors="dracovolans@gmail.com"


# Install Apache and other dependencies
RUN apt-get update && \
    apt-get install -y apache2 && \
    a2enmod proxy proxy_http proxy_wstunnel

# Copy HTML content into Apache's web directory
COPY webapp /var/www/html



# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt /app/


# Install any dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . /app/

EXPOSE 80/tcp
EXPOSE 8000/tcp

# Command to run your application
CMD ["runapi.sh","&&","/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
