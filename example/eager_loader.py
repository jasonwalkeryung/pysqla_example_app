from sqlalchemy.orm import Load, joinedload

from example import database
from example.models import LineItem, Order, SupplierFragment, Variant

print("Eager loading an order")
with database.session() as session:
    # pylint: disable=no-member
    query = session.query(Order).options(
        joinedload(Order.supplier_fragments, innerjoin=True)
            .joinedload(SupplierFragment.line_items, innerjoin=True)
            .joinedload(LineItem.variant, innerjoin=True)
            .joinedload(Variant.product, innerjoin=True),
        Load(Order).raiseload('*')
    ).filter(Order.accepted.is_(True))  # yapf: disable

    query = query.filter(Order.email == 'customer@example.com')

    query = query.order_by(Order.created_at.desc()).limit(10).offset(0)

    print(query)
