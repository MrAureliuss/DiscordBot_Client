from sqlalchemy import create_engine, MetaData

engine = create_engine("postgresql://postgres:qwerty12345@localhost:5432/discordbotDB")

meta = MetaData()


def create_all(_engine):
    meta.create_all(engine)
