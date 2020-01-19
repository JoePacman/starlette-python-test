To run mock_service, within the directory run:
docker build --tag mock-service .
docker run --name mock-service-run -p 5000:5000 mock-service

To run webhook_emulator, within the directory run:
docker build --tag webhook-emulator .
docker run --name webhook-emulator-run -p 8080:8080 webhook-emulator

TODO - insert calling instructions
