from db.SessionHolder import SessionHolder
from db.CreateDBEngine import engine
from db.models.Blacklist import blacklist
from sqlalchemy import select

session_holder = SessionHolder(engine=engine)


def user_not_in_blacklist(ctx):
    session = session_holder.session
    stmt = select(blacklist).where(
        blacklist.c.channelid == str(ctx.message.guild.id),
        blacklist.c.userid == int(ctx.message.author.id)
    )

    row_count = session.execute(stmt).rowcount
    return False if row_count == 1 else True
