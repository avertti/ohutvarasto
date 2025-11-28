from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()


class Warehouse(Base):
    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    capacity = Column(Float, default=0.0)

    items = relationship("Item", back_populates="warehouse", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Warehouse(id={self.id}, name='{self.name}', capacity={self.capacity})>"


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Float, default=0.0)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)

    warehouse = relationship("Warehouse", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', quantity={self.quantity})>"


def init_db(db_url='sqlite:///warehouse.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
