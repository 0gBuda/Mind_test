from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Message


async def create_message(db: AsyncSession, sender_id: int, receiver_id: int, content: str):
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message


async def get_message(db: AsyncSession, sender_id: int, receiver_id: int):
    query = select(Message).where(
        ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
    )
    result = await db.execute(query)
    return result.scalars().all()


