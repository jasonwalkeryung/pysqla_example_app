from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://localhost/example')
Session = sessionmaker(bind=engine)


@contextmanager
def session():
    _session = Session()
    try:
        yield _session
        _session.commit()
    except Exception:  # pylint: disable=broad-except
        _session.rollback()
        raise
    finally:
        _session.close()
