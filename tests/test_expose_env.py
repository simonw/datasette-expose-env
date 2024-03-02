from datasette_test import Datasette
import pytest


@pytest.fixture
def patched(monkeypatch):
    monkeypatch.setenv("FOO", "foo")
    monkeypatch.setenv("BAR", "bar")
    monkeypatch.setenv("BAZ", "baz")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config,expect_foo_and_bar,expect_baz",
    (
        (None, False, False),
        (["FOO", "BAR"], True, False),
        ({"variables": ["FOO", "BAR"]}, True, False),
        (["FOO", "BAR", "BAZ"], True, True),
    ),
)
async def test_env(patched, config, expect_foo_and_bar, expect_baz):
    plugin_config = {}
    if config:
        plugin_config["datasette-expose-env"] = config
    datasette = Datasette(plugin_config=plugin_config)
    response = await datasette.client.get("/-/env")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    if not config:
        assert "No environment variables exposed" in response.text
    if expect_foo_and_bar:
        assert "FOO=foo" in response.text
        assert "BAR=bar" in response.text
    else:
        assert "FOO=foo" not in response.text
        assert "BAR=bar" not in response.text
    if expect_baz:
        assert "BAZ=baz" in response.text
    else:
        assert "BAZ=baz" not in response.text


@pytest.mark.asyncio
async def test_show_all_redacted(patched):
    datasette = Datasette(
        plugin_config={
            "datasette-expose-env": {
                "show_all_redacted": True,
                "variables": ["FOO"],
            }
        }
    )
    response = await datasette.client.get("/-/env")
    assert response.status_code == 200
    assert "FOO=foo" in response.text
    assert "BAR=..." in response.text
    assert "BAZ=..." in response.text
