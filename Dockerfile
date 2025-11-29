# Use an official lightweight Python image
FROM python:3.9-slim

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the application directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose port 8000
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
