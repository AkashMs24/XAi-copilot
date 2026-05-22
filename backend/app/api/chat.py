from fastapi import APIRouter
from app.models.schemas import ChatMessage
from app.services.groq_service import chat_with_copilot

router = APIRouter()


@router.post("/chat")
async def chat(message: ChatMessage):
    response = await chat_with_copilot(
        user_message=message.message,
        application_context=message.application_context,
        conversation_history=message.conversation_history or [],
    )
    return {"response": response}
