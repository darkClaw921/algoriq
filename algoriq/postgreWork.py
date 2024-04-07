import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class UserMessage(Base):
    __tablename__ = 'user_messages'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    nickname = Column(String)
    message_text = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)

    def __repr__(self):
        return f"<UserMessage(chat_id={self.chat_id}, nickname={self.nickname}, message_text={self.message_text}, status={self.status}, sent_at={self.sent_at})>"

DATABASE_URL = 'postgresql://username:password@localhost/database_name'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)

def save_user_message(chat_id, nickname, message_text, status):
    session = Session()
    user_message = UserMessage(chat_id=chat_id, nickname=nickname, message_text=message_text, status=status)
    session.add(user_message)
    session.commit()
    session.close()

def main():
    create_tables()

    # Ваш код для работы с ботом, здесь можно вставить вызов функции save_user_message() для сохранения сообщений

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
