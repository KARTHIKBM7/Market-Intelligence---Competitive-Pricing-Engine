# 1. Base Image: Start with a lightweight version of Python
FROM python:3.9-slim

# 2. Work Directory: Create a folder inside the container
WORKDIR /app

# 3. Copy Files: Move requirements.txt first (for caching speed)
COPY requirements.txt .

# 4. Install Dependencies: Run pip install inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Code: Move the rest of your code (api.py, main.py, etc.)
COPY . .

# 6. Expose Port: Tell the container to listen on port 8000
EXPOSE 8000

# 7. Start Command: What to run when the container starts?
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]