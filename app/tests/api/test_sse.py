def test_message_stream(client):
    timeout = 2
    with client.stream("GET", "sse/stream", params={"timeout": timeout}) as response:
        assert response.status_code == 200

        lines = []
        for line in response.iter_lines():
            if line:
                lines.append(line)
            if len(lines) >= timeout:
                break

    assert lines[0] == "data: 0"
    assert lines[1] == "data: 1"
