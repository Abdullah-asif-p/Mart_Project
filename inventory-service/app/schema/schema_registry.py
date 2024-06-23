from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

from . import inventory_schema_pb2


# Schema Registry
schema_registry_conf = {"url": "http://schema-registry:8081"}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)


protobuf_schema_str = """
syntax = "proto3";

message InventoryItem{

  int32 id = 1;
  string product_id = 2;
  string name = 3;
  string quantity = 4;
  string status = 5;
}



"""


# Function to register schema
def register_schema(subject_name, schema_str):
    schema = Schema(schema_str, "PROTOBUF")
    schema_id = schema_registry_client.register_schema(subject_name, schema)
    return schema_id


# Register the Protobuf schema
subject = "InventoryItem-value"
try:
    schema_id = register_schema(subject, protobuf_schema_str)
    print(f"Schema registered with ID: {schema_id}")
except Exception as e:
    print(f"Schema registration failed: {e}")

protobuf_serializer = ProtobufSerializer(
    inventory_schema_pb2.InventoryItem(),
    schema_registry_client,
    conf={"use.deprecated.format": False},
)
