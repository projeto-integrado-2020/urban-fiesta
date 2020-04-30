import pytest

from no12 import create_app


@pytest.fixture
def client():
    """ Creates a app and expose the Werkzeug test Client. """
    app = create_app("testing")
    yield app.test_client()


def test_list_current_events(client):
    rv = client.get("/eventos")

    assert b"Nenhum evento por enquanto." in rv.data
