import asyncio

from dotenv import load_dotenv

from db import MentionEdge

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from itertools import islice

from db.connector import get_async_session
from parser.parse import extractor

load_dotenv()


async def bulk_upsert_mentions(session: AsyncSession, mentions_list: list[dict],
                               batch_size: int = 1000) -> None:

    def chunked_iterable(iterable, size):
        it = iter(iterable)
        while chunk := list(islice(it, size)):
            yield chunk

    for batch in chunked_iterable(mentions_list, batch_size):
        stmt = pg_insert(MentionEdge).values(batch)

        update_stmt = stmt.on_conflict_do_update(
            index_elements=["source_username", "target_username"],
            set_={"weight": MentionEdge.weight + 1}
        )

        await session.execute(update_stmt)
        await session.commit()


if __name__ == '__main__':
    async def main():
        async with get_async_session() as session:
            mentions = extractor()
            await bulk_upsert_mentions(session, mentions,
                                       batch_size=1000)


    asyncio.run(main())