# Use a stable and lightweight Python image.
FROM python:3.11-slim as base

# Set environment variables to configure Python and pip behavior.
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    QR_CODE_DIR=/myapp/qr_codes

# Set the working directory inside the container
WORKDIR /myapp

# Install system dependencies required for Python and PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to leverage Docker caching
COPY ./requirements.txt /myapp/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Add a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Copy application source code into the container
COPY --chown=myuser:myuser . /myapp

# Expose the FastAPI port
EXPOSE 8000
