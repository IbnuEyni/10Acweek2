FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY rubric/ rubric/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create audit output directories
RUN mkdir -p audit/{report_bypeer_received,report_onpeer_generated,report_onself_generated,langsmith_logs}

# Set environment
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "src.main"]
