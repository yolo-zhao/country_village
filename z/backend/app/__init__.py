from app.controllers.order import bp as order_bp
app.register_blueprint(order_bp, url_prefix='/api') 