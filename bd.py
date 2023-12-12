# Подключение к серверу PostgreSQL на localhost с помощью psycopg2 DBAPI
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, select

from Entity.User import User

# admin202 - пароль для пользователя postgres
engine = create_engine("postgresql+psycopg2://postgres:admin202@localhost/hospital")

engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

print(engine)
"""
user1 = User(
    name = 'Дмитрий Смирнов',
    phone = '8 (910) 856-56-65',
)

user2 = User(
    name = 'Андрей Тарасов',
    phone = '8 (915) 456-26-61',
)

session.add_all([user1, user2])
session.commit()

stmt1 = select(User)

for user in session.scalars(stmt1):
    print(user)
"""