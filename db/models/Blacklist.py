from sqlalchemy import Table, Column, TIMESTAMP, BIGINT, VARCHAR
from db.CreateDBEngine import meta

blacklist = Table(
    'blacklist', meta,
    Column('id', BIGINT, primary_key=True),
    Column('channelid', VARCHAR),
    Column('date_time', TIMESTAMP),
    Column('user_name', VARCHAR),
    Column('userid', BIGINT)
)
