def test_websocket_echo_endpoint(client):
    with client.websocket_connect("/ws/echo") as websocket:
        websocket.send_text("ping")
        
        assert websocket.receive_text() == "ping"
