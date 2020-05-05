import pytest

from no12.models import User
from no12.extensions import db


@pytest.fixture
def test_db():
    return db.test_database


def test_add_new_user(test_db):
    new_user = User(
        email="felipepinto@gmail.com", first_name="Felipe", last_name="Pinto"
    )
    assert new_user.email == "felipepinto@gmail.com"
    assert new_user.first_name == "Felipe"
    assert new_user.last_name == "Pinto"
