## Project Structure

```plaintext
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   ├── main.py
│   ├── kafka/
│   │   ├── __init__.py
│   │   ├── consumer.py
│   │   ├── producer.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── db.py  # Database connection setup
│   │   ├── settings.py  # Configuration settings
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── inventory_crud.py  # CRUD operations for inventory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model.py  # SQLAlchemy models
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── schema_pb2.py  # Auto-generated Python code from Protobuf
│   │   ├── schema.proto  # Protobuf schema definition
│   │   ├── schema_registry.py  # Schema registry logic
│   ├── __init__.py
│   ├── main.py  # Application entry point
├── tests/  # Unit and integration tests
├── .env  # Environment variables
├── Dockerfile  # Docker configuration for containerization
├── pyproject.toml  # Project dependencies and configurations
├── README.md  # Project documentation
```
