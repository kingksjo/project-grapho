# --- Stage 1: Base Image ---
# Use an official Python runtime as a parent image.
# We use a specific version for reproducibility. '-slim' is a smaller image, great for production.
FROM python:3.10-slim

# --- Set the Working Directory ---
# Sets the working directory inside the container to /app. All subsequent commands will be run from this path.
# This keeps our project files organized within the container.
WORKDIR /app

# --- Install Dependencies ---
# Copy the requirements file first, separate from the rest of the code.
# This takes advantage of Docker's layer caching. If our requirements don't change, this layer won't be rebuilt.
COPY requirements.txt .

# Upgrade pip and install the Python dependencies.
# --no-cache-dir makes the image smaller by not storing the download cache.
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# --- Copy Application Code ---
# Now, copy the application code (everything in the 'app' sub-directory) into the container's /app directory.
# Because this is a separate step, any changes to our Python code will only invalidate this layer,
# not the dependency installation layer above, making builds much faster.
COPY ./app /app

# --- Run the Application ---
# This is the command that will be run when a container is started from this image.
# We use uvicorn to run our FastAPI application.
# 'app.main:app' means "in the 'app' directory, find the 'main.py' file, and inside it, find the object named 'app'".
# 'host="0.0.0.0"' is CRUCIAL. It tells the server to listen for connections on all network interfaces inside the container,
# which is necessary to expose it to the outside world.
# '--reload' is great for development, as it automatically restarts the server when you change the code.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]