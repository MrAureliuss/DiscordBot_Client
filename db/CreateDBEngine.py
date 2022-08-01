from sqlalchemy import create_engine, MetaData

engine = create_engine("postgresql://postgres:qwerty12345@localhost:5432/discordbotDB")

meta = MetaData()
meta.create_all(engine)
