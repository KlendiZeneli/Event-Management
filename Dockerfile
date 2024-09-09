FROM python:3.12.5
EXPOSE 5000
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]