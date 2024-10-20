from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .crud import create_message, get_message
from .schemas import MessageCreate, MessageResponse
from ..auth.routes import get_current_user
from ..auth.models import User
from app.websocket.websockets import ConnectionManager

router = APIRouter()
manager = ConnectionManager


@router.post("/send", response_model=MessageResponse)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    new_message = await create_message(db, sender_id=current_user.id, receiver_id=message.receiver_id,
                                       content=message.content)
    return new_message


@router.get("/history/{receiver_id}", response_model=List[MessageResponse])
async def get_message_history(receiver_id: int, current_user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    messages = await get_message(db, sender_id=current_user.id, receiver_id=receiver_id)
    return messages


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User {user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {user_id} left the chat")
