from datetime import datetime
from app import db
from app.models.user import User
from app.models.product import Product

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(32), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_fee = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, completed, cancelled
    payment_method = db.Column(db.String(20))
    carrier = db.Column(db.String(50))
    tracking_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    shipped_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)

    # 关联
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True)
    address = db.relationship('OrderAddress', backref='order', uselist=False)

    def __init__(self, user_id, total_amount, shipping_fee=0):
        self.user_id = user_id
        self.total_amount = total_amount
        self.shipping_fee = shipping_fee
        self.order_number = self.generate_order_number()

    def generate_order_number(self):
        """生成订单号"""
        import random
        import string
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f'{timestamp}{random_str}'

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'total_amount': float(self.total_amount),
            'shipping_fee': float(self.shipping_fee),
            'status': self.status,
            'payment_method': self.payment_method,
            'carrier': self.carrier,
            'tracking_number': self.tracking_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'items': [item.to_dict() for item in self.items],
            'address': self.address.to_dict() if self.address else None
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # 关联
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': float(self.price),
            'product': self.product.to_dict()
        }

class OrderAddress(db.Model):
    __tablename__ = 'order_addresses'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'receiver': self.receiver,
            'phone': self.phone,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'address': self.address,
            'is_default': self.is_default
        } 