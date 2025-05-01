from flask import Blueprint, request, jsonify, g
from app.models.order import Order, OrderItem, OrderAddress
from app.models.product import Product
from app import db
from app.utils.auth import login_required
from app.utils.response import success, error
from datetime import datetime

bp = Blueprint('order', __name__)

@bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    """获取订单列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    status = request.args.get('status')

    query = Order.query.filter_by(user_id=g.user.id)
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    orders = [order.to_dict() for order in pagination.items]
    
    return success({
        'orders': orders,
        'total': pagination.total,
        'page': page,
        'pageSize': page_size
    })

@bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order_detail(order_id):
    """获取订单详情"""
    order = Order.query.filter_by(id=order_id, user_id=g.user.id).first_or_404()
    return success(order.to_dict())

@bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    """创建订单"""
    data = request.get_json()
    
    # 验证商品
    items = data.get('items', [])
    if not items:
        return error('订单商品不能为空')
    
    # 计算总金额
    total_amount = 0
    for item in items:
        product = Product.query.get_or_404(item['product_id'])
        if product.stock < item['quantity']:
            return error(f'商品 {product.name} 库存不足')
        total_amount += product.price * item['quantity']
    
    # 创建订单
    order = Order(
        user_id=g.user.id,
        total_amount=total_amount,
        shipping_fee=data.get('shipping_fee', 0)
    )
    db.session.add(order)
    
    # 创建订单商品
    for item in items:
        product = Product.query.get(item['product_id'])
        order_item = OrderItem(
            order=order,
            product_id=product.id,
            quantity=item['quantity'],
            price=product.price
        )
        # 更新商品库存
        product.stock -= item['quantity']
        db.session.add(order_item)
    
    # 创建订单地址
    address_data = data.get('address')
    if address_data:
        order_address = OrderAddress(
            order=order,
            receiver=address_data['receiver'],
            phone=address_data['phone'],
            province=address_data['province'],
            city=address_data['city'],
            district=address_data['district'],
            address=address_data['address'],
            is_default=address_data.get('is_default', False)
        )
        db.session.add(order_address)
    
    try:
        db.session.commit()
        return success(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return error('创建订单失败')

@bp.route('/orders/<int:order_id>/pay', methods=['POST'])
@login_required
def pay_order(order_id):
    """支付订单"""
    order = Order.query.filter_by(id=order_id, user_id=g.user.id).first_or_404()
    
    if order.status != 'pending':
        return error('订单状态不正确')
    
    data = request.get_json()
    payment_method = data.get('payment_method')
    if not payment_method:
        return error('请选择支付方式')
    
    # 这里应该调用实际的支付接口
    # 为了演示，我们直接模拟支付成功
    order.status = 'paid'
    order.payment_method = payment_method
    order.paid_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return success(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return error('支付失败')

@bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """取消订单"""
    order = Order.query.filter_by(id=order_id, user_id=g.user.id).first_or_404()
    
    if order.status != 'pending':
        return error('只有待支付的订单才能取消')
    
    order.status = 'cancelled'
    order.cancelled_at = datetime.utcnow()
    
    # 恢复商品库存
    for item in order.items:
        product = item.product
        product.stock += item.quantity
    
    try:
        db.session.commit()
        return success(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return error('取消订单失败')

@bp.route('/orders/<int:order_id>/confirm', methods=['POST'])
@login_required
def confirm_receipt(order_id):
    """确认收货"""
    order = Order.query.filter_by(id=order_id, user_id=g.user.id).first_or_404()
    
    if order.status != 'shipped':
        return error('订单状态不正确')
    
    order.status = 'completed'
    order.completed_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return success(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return error('确认收货失败')

@bp.route('/orders/<int:order_id>/ship', methods=['POST'])
@login_required
def ship_order(order_id):
    """发货"""
    # 检查用户是否为农户
    if not g.user.is_farmer:
        return error('只有农户才能发货')
    
    order = Order.query.filter_by(id=order_id).first_or_404()
    
    if order.status != 'paid':
        return error('订单状态不正确')
    
    data = request.get_json()
    carrier = data.get('carrier')
    tracking_number = data.get('tracking_number')
    
    if not carrier or not tracking_number:
        return error('请填写物流信息')
    
    order.status = 'shipped'
    order.carrier = carrier
    order.tracking_number = tracking_number
    order.shipped_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return success(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return error('发货失败') 