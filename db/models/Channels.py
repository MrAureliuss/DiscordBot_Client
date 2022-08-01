from sqlalchemy import Table, Column, Integer, Boolean, TIMESTAMP, BIGINT, VARCHAR
from db.CreateDBEngine import meta

channel = Table(
    'channels', meta,
    Column('id', BIGINT, primary_key=True),
    Column('active', Boolean),
    Column('channelid', VARCHAR),
    Column('display_name', VARCHAR),
    Column('local_date_time', TIMESTAMP),
    Column('registrationuuidtoken', VARCHAR),
    Column('owner_id', BIGINT)
)
