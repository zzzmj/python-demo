import socket


def route_index():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_img():
    """
    图片的处理函数, 读取图片并生成响应返回
    """
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/': route_index,
        '/doge.gif': route_img,
    }
    # 这里得到的是一个函数体
    response = r.get(path)
    return response()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化socket
    with socket.socket() as s:
        s.bind((host, port))
        # 监听 接收 读取请求数据
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024).decode('utf-8')
            print('ip = {}\nrequest = {}'.format(address, request))
            try:
                # 得到HTTP请求的路径
                path = request.split()[1]
                # 根据路径返回响应
                response = response_for_path(path)
                # 响应给客户端(浏览器)
                connection.sendall(response)
            except Exception as e:
                print('error', e)


if __name__ == "__main__":
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
