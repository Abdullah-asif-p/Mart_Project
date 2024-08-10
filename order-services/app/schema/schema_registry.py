from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

from app.schema import order_pb2


# Schema Registry
schema_registry_conf = {"url": "http://schema-registry:8081"}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)


protobuf_schema_str = """
syntax = "proto3";

message Status {
  enum Value {
    PENDING_PAYMENT = 0;
    COMPLETED = 1;
    SHIPPED = 2;
    CANCELLED = 3;
  }
  Value value = 1;
}

message Order {
  string id = 1;
  string user_id = 2;
  string product_id = 3;
  int32 quantity = 4;
  int32 total_amount = 5;
  string status = 6;
  string created_at = 7;
}
"""


# Function to register schema
def register_schema(subject_name, schema_str):
    schema = Schema(schema_str, "PROTOBUF")
    schema_id = schema_registry_client.register_schema(subject_name, schema)
    return schema_id


# Register the Protobuf schema
subject = "todo-value"
try:
    schema_id = register_schema(subject, protobuf_schema_str)
    print(f"Schema registered with ID: {schema_id}")
except Exception as e:
    print(f"Schema registration failed: {e}")

protobuf_serializer = ProtobufSerializer(
    order_pb2.Order, schema_registry_client, conf={"use.deprecated.format": False}
)
