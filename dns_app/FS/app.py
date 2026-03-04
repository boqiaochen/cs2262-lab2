from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()
    if not data:
        return "Bad Request: No JSON body\n", 400

    hostname = data.get("hostname")
    ip = data.get("ip")
    as_ip = data.get("as_ip")
    as_port = data.get("as_port")

    if not all([hostname, ip, as_ip, as_port]):
        return "Bad Request: Missing fields\n", 400

    dns_message = (
        f"TYPE=A\n"
        f"NAME={hostname}\n"
        f"VALUE={ip}\n"
        f"TTL=10\n"
    )

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(dns_message.encode("utf-8"), (as_ip, int(as_port)))
        sock.close()
        print(f"[FS] Registered {hostname} -> {ip} with AS at {as_ip}:{as_port}")
    except Exception as e:
        return f"Registration failed: {e}\n", 500

    return "Registered successfully\n", 201

@app.route("/fibonacci", methods=["GET"])
def get_fibonacci():
    number_str = request.args.get("number")
    if number_str is None:
        return "Bad Request: Missing 'number' parameter\n", 400

    try:
        number = int(number_str)
    except ValueError:
        return "Bad Request: 'number' must be an integer\n", 400

    result = fibonacci(number)
    return jsonify({"fibonacci": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
