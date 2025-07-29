# Single-stage build using Python 3.12
FROM registry.access.redhat.com/ubi9/python-312

# Switch to root user temporarily for installations
USER 0

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set uv environment variables
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# Create the Python site-packages directory for the app-root user
RUN mkdir -p /opt/app-root/lib/python3.12/site-packages && \
    mkdir -p /opt/app-root/lib64/python3.12/site-packages

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies using uv pip with app-root target
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python /usr/bin/python3.12 --target /opt/app-root/lib/python3.12/site-packages -r pyproject.toml

# Change ownership to the default user (1001 in UBI images)
RUN chown -R 1001:0 /app /opt/app-root && chmod -R g=u /app /opt/app-root

# Switch to non-root user (UBI default user)
USER 1001

# Run the MCP server app
CMD ["python3.12", "main.py"]
