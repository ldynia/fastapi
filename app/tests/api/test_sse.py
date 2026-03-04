def test_sse_stream_endpoint(client):
	with client.stream("GET", "/sse/stream", params={"timeout": 2}) as response:
		assert response.status_code == 200
		assert response.headers["content-type"].startswith("text/event-stream")

		lines = []
		for line in response.iter_lines():
			if line:
				lines.append(line)
			if len(lines) >= 3:
				break

	assert lines[0] == "data: 0"
	assert lines[1] == "data: 1"
	assert lines[2] == "data: 2"
