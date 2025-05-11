from dataclasses import dataclass
from ipv8.messaging.payload_dataclass import DataClassPayload
from ipv8.messaging.serialization import default_serializer

@dataclass
class Transaction(DataClassPayload[1]):
    sender_mid: bytes
    receiver_mid: bytes
    cert_hash: bytes
    timestamp: float
    signature: bytes
    public_key: bytes

    @classmethod
    def serializer(cls):
        return default_serializer(cls, [
            (bytes, "sender_mid"),
            (bytes, "receiver_mid"),
            (bytes, "cert_hash"),
            (float, "timestamp"),
            (bytes, "signature"),
            (bytes, "public_key"),
        ])
