config = {
    "kafka": {
        "servers": "192.168.2.53:29092",
        "conf": {
            "bootstrap.servers": "192.168.2.53:29092",
            "acks": 0,
            # "buffer.memory": 1554432,
            "batch.size": 1,
            "queue.buffering.max.ms": 5
        },
        "topics": {
            "Sting"
        }
    },
    "i2c": {
        "cmd": {
            "move": 0x01,
            "idle": 0x02,
            "reset": 0x03,
            "autoidleon": 0x04,
            "autoidleoff": 0x05,
        },
        "address": {
            "servoController": 0x08
        }
    }
}
