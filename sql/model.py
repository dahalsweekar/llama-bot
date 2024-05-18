from .database import Base, engine
from sqlalchemy import Column, LargeBinary, Integer


class PDF(Base):
    __tablename__ = 'pdf'

    id = Column(Integer, primary_key=True, index=True)
    file_data = Column(LargeBinary, nullable=False)


Base.metadata.create_all(bind=engine)
