import socket
import json
import os

DNS_RECORDS_FILE = "dns_records.json"

def load_records():
    if os.path.exists(DNS_RECORDS_FILE):
        with open(DNS_RECORDS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_records(records):
    with open(DNS_RECORDS_FILE, "w") as f:
        json.dump(records, f)

def parse_message(message):
    fields = {}
    lines = message.strip().split("\n")
    for line in lines:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            fields[key.strip()] = value.strip()
    return fields

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 53533))
    print("[AS] Authoritative Server started on UDP port 53533")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode("utf-8")
        print(f"[AS] Received from {addr}: {message}")

        fields = parse_message(message)
        records = load_records()

        if "VALUE" in fields:
            name = fields.get("NAME", "")
            value = fields.get("VALUE", "")
            record_type = fields.get("TYPE", "A")
            ttl = fields.get("TTL", "10")
            records[name] = {"VALUE": value, "TYPE": record_type, "TTL": ttl}
            save_records(records)
            print(f"[AS] Registered: {name} -> {value}")
        else:
            name = fields.get("NAME", "")
            if name in records:
                record = records[name]
                response = (
                    f"TYPE={record['TYPE']}\n"
                    f"NAME={name}\n"
                    f"VALUE={record['VALUE']}\n"
                    f"TTL={record['TTL']}\n"
                )
                sock.sendto(response.encode("utf-8"), addr)
                print(f"[AS] Query {name} -> {record['VALUE']}")
            else:
                print(f"[AS] Query {name} -> NOT FOUND")

if __name__ == "__main__":
    main()
