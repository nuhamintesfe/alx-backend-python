# Use Python 3.10 base image
FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files into container
COPY . .

# Expose Django default port 8000
EXPOSE 8000

# Command to run Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

