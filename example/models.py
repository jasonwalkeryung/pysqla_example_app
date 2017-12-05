"""
DO NOT USE THESE IN PRODUCTION!!!

This is a simplified version of our schema for illustrative purposes.
This allows us to code out examples for the blog without having
to reveal any proprietary information.

Needless to say this isn't part of the normal migration cycle,
so if you should ever have to make any changes, here's the commands:
```
alembic -c alembic__example.ini revision --autogenerate -m "Initial revision"
alembic -c alembic__example.ini upgrade head
```

DO NOT USE THESE IN PRODUCTION!!!
"""
import re

from sqlalchemy import (
    Column, Integer, String, DateTime, Numeric, FetchedValue, ForeignKey, Text, Boolean
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship

Model = declarative_base()


class ExampleModel(Model):
    __abstract__ = True

    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')

    id = Column(Integer, primary_key=True, server_default=FetchedValue())

    @classmethod
    def camel_case_name(cls):
        """Convert to camel case."""
        s1 = cls.first_cap_re.sub(r'\1_\2', cls.__name__)
        return cls.all_cap_re.sub(r'\1_\2', s1).lower()

    # pylint: disable=no-self-argument
    @declared_attr
    def __tablename__(cls):
        return "example_{}s".format(cls.camel_case_name())


class Product(ExampleModel):
    name = Column(String, nullable=False)
    description = Column(Text)
    list_price = Column(Numeric)
    sell_price = Column(Numeric)
    variants = relationship('Variant', backref="product")


class Variant(ExampleModel):
    product_id = Column(ForeignKey('example_products.id'))
    inventory = relationship('Inventory')


class Inventory(ExampleModel):
    variant_id = Column(ForeignKey('example_variants.id'))
    available_to_sell = Column(Integer, nullable=False)


class User(ExampleModel):
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())


class Order(ExampleModel):
    user_id = Column(ForeignKey('example_users.id'))
    email = Column(String)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    shipping_address = Column(JSONB, nullable=False)

    item_subtotal = Column(Numeric)
    tax = Column(Numeric)
    total = Column(Numeric)

    accepted = Column(Boolean)

    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    source = Column(String)

    supplier_fragments = relationship('SupplierFragment', backref="order")


class SupplierFragment(ExampleModel):
    supplier_id = Column(ForeignKey('example_orders.id'))

    line_items = relationship('LineItem', backref="supplier_fragment")


class LineItem(ExampleModel):
    supplier_fragment_id = Column(ForeignKey('example_supplier_fragments.id'))
    variant_id = Column(ForeignKey('example_variants.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric)
    tax = Column(Numeric)

    variant = relationship('Variant', backref="line_item", uselist=False)
