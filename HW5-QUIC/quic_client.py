class QUICClient:
    def connect(socket_addr: tuple[str, int]):
        """connect to the specific server"""
        pass

    def send(stream_id: int, data: bytes):
        """call this method to send data, with non-reputation stream_id"""
        pass

    def recv() -> tuple[int, bytes]: # stream_id, data
        """receive a stream, with stream_id"""
        pass

    def close():
        """close the connection and the socket"""
        pass
