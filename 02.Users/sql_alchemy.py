from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database
engine = create_engine("sqlite:///users.db")
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)


# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# https://stackoverflow.com/questions/58936116/pycharm-warns-about-unexpected-arguments-for-sqlalchemy-user-model
# Add a user
new_user = User(
    firstname="John",
    lastname="Doe",
    username="johndoe",
    email="johndoe@example.com",
    password="123456",
    age=30,
)
session.add(new_user)
session.commit()

# Query the database
all_users = session.query(User).all()
for user in all_users:
    print(user.firstname, user.lastname)
