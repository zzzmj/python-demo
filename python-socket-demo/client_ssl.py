# 用原生socket实现一个具有基本功能的socket, 并抓取了豆瓣top250的数据
import socket
import ssl


def parse_url(url):
    """
    解析 url 返回 (protocol host port path)
    """
    protocol = 'http'
    i = url.find('://')
    if i == -1:
        u = url
    else:
        protocol = url[0:i]
        u = url.split('://')[1]
    # 2. 解析host和path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 3.解析端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    # print('protocol = {}\nhost = {}\nport = {}\nsearch = {}\n------------'.format(protocol, host, port, path))
    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parse_response(r):
    """
    解析responce, 返回一个(status_code, headers, body)
    """
    headers, body = r.split('\r\n\r\n', 1)
    h = headers.split('\r\n')
    status_code = int(h[0].split(" ")[1])

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


def get(url):
    """
    用get访问一个url地址, 并返回响应(status_code, headers, body)
    """
    protocol, host, port, path = parse_url(url)
    s = socket_by_protocol(protocol)

    s.connect((host, port))
    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(
        path, host)
    s.send(request.encode('utf-8'))

    responce = response_by_socket(s).decode('utf-8')
    status_code, headers, body = parse_response(responce)

    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)
    return status_code, headers, body


if __name__ == "__main__":
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)
    print(body)
