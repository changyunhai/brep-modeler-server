# 本文件仅用于DEBUG。

# 8810端口 - socketIO
# 8811端口 - 管理端口, 用于socket连接的监控和后台管理

# 在实际部署中, 仅需要启动8810端口, 后台监控程序为可选, 不是必须

# 本地开发请使用命令行：
#   python -m uvicorn app_sio:app --port 8810 --reload
#   python -m uvicorn app_http:app --port 8811 --reload

# 线上部署使用命令行启动服务：
#   python -m uvicorn app_sio:app --port 8810
#   python -m uvicorn app_http:app --port 8811

if __name__ == '__main__':
    import uvicorn
    import warnings

    warnings.warn("ONLY used in DEBUG mode, DO NOT use in production.")
    sio_server: bool = True

    if sio_server:
        from app_sio import app as app_sio

        uvicorn.run(app_sio, host="0.0.0.0", port=8810)
    else:
        from app_http import app as app_http

        uvicorn.run(app_http, host="0.0.0.0", port=8811)
