from flask import Flask, request
import socket
import requests as http_requests

app = Flask(__name__)

def dns_query(hostname, as_ip, as_port):
    query_message = (
        f"TYPE=A\n"
        f"NAME={hostname}\n"
    )
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(query_message.encode("utf-8"), (as_ip, int(as_port)))
        data, _ = sock.recvfrom(1024)
        sock.close()
        response = data.decode("utf-8")
        for line in response.strip().split("\n"):
            if line.strip().startswith("VALUE="):
                return line.strip().split("=", 1)[1]
        return None
    except Exception as e:
        print(f"[US] DNS query failed: {e}")
        return None

@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request: Missing parameters\n", 400

    fs_ip = dns_query(hostname, as_ip, as_port)
    if not fs_ip:
        return "DNS query failed\n", 500

    try:
        fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        response = http_requests.get(fs_url, timeout=5)
        return response.text, response.status_code
    except Exception as e:
        return f"Failed to reach Fibonacci Server: {e}\n", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
