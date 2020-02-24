import nox
from nox.sessions import Session


@nox.session(python=["3.8", "3.7"])
def tests(session: Session) -> None:
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.run("poetry", "install", external=True)
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
