FROM python:alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH=/usr/local/bin/python:$PATH
ENV PYTHONPATH=/app/:$PYTHONPATH

# Install nodejs
RUN apk add --update nodejs

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the rest of your application's code
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Define the command to run your application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
