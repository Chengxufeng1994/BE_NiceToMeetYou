FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
      curl \
      vim \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -\
  && poetry config virtualenvs.in-project true

# Install dependencies (runtime only)
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-root

# Copy the entire project
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD [ "poetry", "run", "fastapi", "run" ]
