from cli import screen_manager

admin_client_config = {"bootstrap.servers": "kafka:9092"}

screen_manager.display(admin_client_config, timeout=10)
