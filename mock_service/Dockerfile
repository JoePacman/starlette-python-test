FROM tiangolo/uvicorn-gunicorn-starlette:python3.7
COPY . /app
WORKDIR /app
RUN pip install starlette uvicorn httpx
RUN pip install prometheus_client
EXPOSE 8080
EXPOSE 8081
EXPOSE 5000
CMD CALLBACK_URL=http://0.0.0.0:5000 python3 mock_service.py
