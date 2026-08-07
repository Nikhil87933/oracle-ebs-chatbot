FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Enable unbuffered logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src ./src

# Install the project
RUN pip install --no-cache-dir -e .

# Default command
CMD ["python", "-c", "from enterprise_template import hello; hello()"]
