from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# FastAPI app
app = FastAPI()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Message model
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    message = Column(String)

Base.metadata.create_all(bind=engine)

# Request body model
class MessageData(BaseModel):
    user: str
    message: str

# POST /send endpoint
@app.post("/send")
async def send_message(data: MessageData):
    db = SessionLocal()
    new_msg = Message(user=data.user, message=data.message)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    db.close()
    return {"status": "Message saved", "id": new_msg.id}

