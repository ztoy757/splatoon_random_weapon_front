FROM node:18-bullseye

# Install Python and related tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -s /usr/bin/python3 /usr/local/bin/python

# Set working directory
WORKDIR /workspace

# Create requirements.txt for Python development
COPY requirements.txt /workspace/requirements.txt

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Install playwright and its dependencies
RUN python -m playwright install --with-deps chromium \
    && playwright install chromium

# Install install claude-code CLI
RUN npm install -g @anthropic-ai/claude-code

# # Set default user
# RUN useradd -m -s /bin/bash vscode && \
#     chown -R vscode:vscode /workspace

# USER vscode

# # Set environment variables
# ENV PYTHONPATH=/workspace
# ENV NODE_ENV=development