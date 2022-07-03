from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("configured", (True, False))
async def test_env(monkeypatch, configured):
    monkeypatch.setenv("FOO", "foo")
    monkeypatch.setenv("BAR", "bar")
    monkeypatch.setenv("BAZ", "baz")
    datasette = Datasette(
        [],
        memory=True,
        metadata={"plugins": {"datasette-expose-env": ["FOO", "BAR"]}}
        if configured
        else {},
    )
    response = await datasette.client.get("/-/env")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    if not configured:
        assert "No environment variables exposed" in response.text
    else:
        assert "FOO=foo" in response.text
        assert "BAR=bar" in response.text
        assert "BAZ=baz" not in response.text
