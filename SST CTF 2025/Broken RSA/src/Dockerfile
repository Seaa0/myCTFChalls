# Use the official Python image
FROM python:3.12-slim

# Copy the app code
COPY . .

# Install required Python packages directly
RUN pip install --no-cache-dir pycryptodome

# Expose the Flask port
EXPOSE 1000

# Start the app
CMD ["python", "server.py"]