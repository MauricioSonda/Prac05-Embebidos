import socket
from datetime import datetime

def parse_http_request(request):
    lines = request.split("\r\n")
    if not lines:
        return {}

    try:
        method, path, version = lines[0].split(" ")
    except ValueError:
        return {}

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

    return {"method": method, "path": path, "headers": headers}

def send_http_response(status, body, headers=None):
    status_text = {200:"OK", 401:"Unauthorized", 403:"Forbidden", 404:"Not Found"}.get(status, "OK")
    header_lines = "Content-Type: text/plain\r\n"
    if headers:
        for k,v in headers.items():
            header_lines += f"{k}: {v}\r\n"
    response = f"HTTP/1.1 {status} {status_text}\r\n{header_lines}\r\n{body}"
    return response.encode("utf-8")

def hora_actual():
    return datetime.now().strftime("%H:%M:%S")

def extract_token_from_authorization(auth_header):
    """
    Authorization: {token:1234}
    """
    if not auth_header:
        return None
    auth_header = auth_header.strip()
    if auth_header.startswith("{") and auth_header.endswith("}"):
        # quitar llaves y separar por :
        content = auth_header[1:-1]
        if content.lower().startswith("token:"):
            return content[6:].strip()
    return None

def handler_path(path, headers):
   
    route = path.lower()

    if route == "/":
        return send_http_response(200, "Hola mundo handler")

    if route == "/api_hora":
        hora = hora_actual()
        return send_http_response(200, f"Respuesta desde /Api_hora: {hora}")

    if route == "/admin":
        auth_header = headers.get("authorization")
        token = extract_token_from_authorization(auth_header)

        if token != "1234":
            return send_http_response(401, "Token inválido o no proporcionado")
        return send_http_response(200, "Bienvenido Admin")

    return send_http_response(404, "Ruta no encontrada")

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(5)
    print("Servidor escuchando en 0.0.0.0:8080")

    try:
        while True:
            client, addr = s.accept()
            data = client.recv(4096).decode("utf-8")
            if not data:
                client.close()
                continue

            parsed = parse_http_request(data)
            path = parsed.get("path", "/")
            headers = parsed.get("headers", {})

            response = handler_path(path, headers)
            client.sendall(response)
            client.close()

    except KeyboardInterrupt:
        print("Servidor detenido")
    finally:
        s.close()

if __name__ == "__main__":
    start_server()
