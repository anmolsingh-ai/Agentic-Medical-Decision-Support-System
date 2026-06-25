from streaming_utils import stream_text


def test_stream_text_yields_chunked_output():
    text = "hello world"
    chunks = list(stream_text(text, chunk_size=3, delay=0.0))

    assert chunks == ["hel", "lo ", "wor", "ld"]


def test_stream_text_handles_empty_input():
    assert list(stream_text("", chunk_size=3, delay=0.0)) == []
