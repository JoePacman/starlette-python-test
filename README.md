To run mock_service, within the directory run:

docker build --tag mock-service .

docker run --name mock-service-run -p 8080:8080 -p 8081:8081 mock-service


To run webhook_emulator, within the directory run:

docker build --tag webhook-receiver .

docker run --name webhook-receiver-run -p 5000:5000 webhook-receiver


TODO - insert calling instructions
