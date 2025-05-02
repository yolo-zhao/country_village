# backend/apps/core/views.py
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os
import uuid
import requests
import json
from datetime import datetime, timedelta
from .models import SystemAnnouncement, Feedback, HelpArticle
from .serializers import SystemAnnouncementSerializer, FeedbackSerializer, HelpArticleSerializer
import logging
import sys

# 添加agent目录到系统路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'agent'))

# 导入agent模块
try:
    from agent.graph_flow import build_graph
    logger = logging.getLogger(__name__)
    logger.info("成功导入AI助手模块")
    AI_ASSISTANT_ENABLED = True
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"导入AI助手模块失败: {str(e)}")
    AI_ASSISTANT_ENABLED = False

# 简单的备用AI响应生成器
class SimpleFallbackAI:
    """当AI助手模块不可用时的备用响应生成器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.response_templates = {
            "greeting": [
                "您好！很高兴为您服务。",
                "您好，有什么可以帮到您的吗？",
                "欢迎使用乡村旅游平台客服。请问有什么可以帮您？"
            ],
            "farewell": [
                "感谢您的咨询，再见！",
                "很高兴能帮到您，祝您旅途愉快！",
                "期待您的下次光临，再见！"
            ],
            "fallback": [
                "抱歉，我目前无法回答这个问题。您可以尝试咨询其他问题或稍后再试。",
                "这个问题有点复杂，建议您联系客服人员获取更准确的信息。",
                "对不起，我还在学习中。这个问题我暂时回答不了。"
            ]
        }
    
    def respond_to(self, message):
        """根据用户消息生成简单的响应"""
        self.logger.info(f"备用AI响应: {message}")
        
        if any(word in message for word in ["你好", "您好", "早上好", "下午好", "晚上好", "嗨", "hi", "hello"]):
            import random
            return random.choice(self.response_templates["greeting"])
        
        if any(word in message for word in ["再见", "拜拜", "谢谢", "感谢", "bye", "thank"]):
            import random
            return random.choice(self.response_templates["farewell"])
        
        # 针对乡村旅游常见问题的简单回复
        if "农产品" in message or "特产" in message:
            return "我们的平台提供多种当地农特产品，您可以在产品页面浏览并购买。"
        
        if "活动" in message:
            return "我们平台提供多种乡村体验活动，包括农耕体验、采摘活动等，您可以在活动页面查看详情并预约。"
        
        if "价格" in message or "费用" in message:
            return "不同活动和产品的价格各不相同，您可以在具体的活动或产品页面查看详细价格信息。"
        
        if "预订" in message or "预约" in message or "怎么订" in message:
            return "您可以在活动详情页点击'立即预约'按钮，填写相关信息后提交预约。我们会尽快处理您的请求。"
        
        if "退款" in message or "取消" in message:
            return "如需取消预约或退款，请在'我的订单'中找到相应订单，点击'申请取消'或'申请退款'按钮。"
        
        # 默认回复
        import random
        return random.choice(self.response_templates["fallback"])

# 创建备用AI实例
fallback_ai = SimpleFallbackAI()

class SystemAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = SystemAnnouncement.objects.all().order_by('-created_at')
    serializer_class = SystemAnnouncementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FileUploadView(APIView):
    """
    文件上传接口
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        file_obj = request.FILES.get('file')
        file_type = request.data.get('type', 'image')
        
        if not file_obj:
            return Response({'error': '没有找到文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 文件类型验证
        allowed_types = {
            'image': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
            'document': ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
            'video': ['video/mp4', 'video/mpeg', 'video/quicktime']
        }
        
        if file_type not in allowed_types:
            return Response({'error': '不支持的文件类型'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查文件MIME类型
        if hasattr(file_obj, 'content_type') and file_obj.content_type not in allowed_types[file_type]:
            return Response({'error': f'文件类型错误，支持的类型: {", ".join(allowed_types[file_type])}'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 生成唯一文件名
        filename = f"{file_type}_{uuid.uuid4().hex}{os.path.splitext(file_obj.name)[1]}"
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_type)
        
        # 确保目录存在
        os.makedirs(upload_path, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_path, filename)
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        
        # 生成文件URL
        file_url = f"{settings.MEDIA_URL}uploads/{file_type}/{filename}"
        
        return Response({
            'url': file_url,
            'file_name': filename,
            'file_type': file_type,
            'size': file_obj.size
        }, status=status.HTTP_201_CREATED)

class FeedbackView(APIView):
    """
    用户反馈接口
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # 只有管理员可以查看所有反馈
        if request.user.is_staff:
            feedbacks = Feedback.objects.all().order_by('-created_at')
            serializer = FeedbackSerializer(feedbacks, many=True)
            return Response(serializer.data)
        # 普通用户只能查看自己的反馈
        else:
            feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
            serializer = FeedbackSerializer(feedbacks, many=True)
            return Response(serializer.data)

class HelpCenterView(APIView):
    """
    帮助中心接口
    """
    def get(self, request):
        article_id = request.query_params.get('id')
        
        if article_id:
            try:
                article = HelpArticle.objects.get(id=article_id)
                serializer = HelpArticleSerializer(article)
                return Response(serializer.data)
            except HelpArticle.DoesNotExist:
                return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 获取分类文章列表
            category = request.query_params.get('category')
            if category:
                articles = HelpArticle.objects.filter(category=category, is_published=True).order_by('-created_at')
            else:
                articles = HelpArticle.objects.filter(is_published=True).order_by('-created_at')
            
            serializer = HelpArticleSerializer(articles, many=True)
            return Response(serializer.data)

class WeatherInfoView(APIView):
    """
    天气信息接口
    """
    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        
        if not latitude or not longitude:
            return Response({'error': '需要提供位置信息 (latitude, longitude)'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 这里应该调用真实的天气API
            # 为演示目的，我们返回模拟数据
            weather_data = {
                'location': '模拟位置',
                'current': {
                    'temperature': 22,
                    'weather': '晴',
                    'wind_speed': 3,
                    'humidity': 65,
                    'updated_at': datetime.now().isoformat()
                },
                'forecast': [
                    {
                        'date': (datetime.now().date() + timedelta(days=i)).isoformat(),
                        'max_temp': 22 + i,
                        'min_temp': 15 + i,
                        'weather': '晴' if i % 2 == 0 else '多云'
                    } for i in range(7)
                ]
            }
            
            return Response(weather_data)
            
        except Exception as e:
            return Response({'error': f'获取天气信息失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardView(APIView):
    """
    控制面板数据接口
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 只允许管理员或农户访问
        if not (request.user.is_staff or hasattr(request.user, 'farmerprofile')):
            return Response({'error': '没有权限访问控制面板'}, status=status.HTTP_403_FORBIDDEN)
        
        # 为管理员返回系统数据
        if request.user.is_staff:
            from django.contrib.auth.models import User
            from django.db.models import Count, Sum
            from django.utils import timezone
            from datetime import timedelta
            
            # 用户统计
            total_users = User.objects.count()
            total_tourists = User.objects.filter(touristprofile__isnull=False).count()
            total_farmers = User.objects.filter(farmerprofile__isnull=False).count()
            
            # 活动统计
            from apps.activities.models import Activity, Reservation
            total_activities = Activity.objects.count()
            total_reservations = Reservation.objects.count()
            
            # 过去7天的新用户数量
            last_week = timezone.now() - timedelta(days=7)
            new_users_last_week = User.objects.filter(date_joined__gte=last_week).count()
            
            return Response({
                'users': {
                    'total': total_users,
                    'tourists': total_tourists,
                    'farmers': total_farmers,
                    'new_last_week': new_users_last_week
                },
                'activities': {
                    'total': total_activities,
                    'reservations': total_reservations
                },
                'system': {
                    'announcements': SystemAnnouncement.objects.filter(is_active=True).count(),
                    'feedbacks': Feedback.objects.filter(status='pending').count()
                }
            })
        
        # 为农户返回个人数据
        else:
            from apps.activities.models import Activity, Reservation
            from django.db.models import Count, Sum
            
            user_activities = Activity.objects.filter(farmer=request.user)
            user_reservations = Reservation.objects.filter(activity__farmer=request.user)
            
            return Response({
                'activities': {
                    'total': user_activities.count(),
                    'reservations': user_reservations.count(),
                    'recent': ActivitySerializer(user_activities.order_by('-created_at')[:5], many=True).data
                },
                'reservations': {
                    'pending': user_reservations.filter(status='pending').count(),
                    'confirmed': user_reservations.filter(status='confirmed').count(),
                    'cancelled': user_reservations.filter(status='cancelled').count(),
                    'completed': user_reservations.filter(status='completed').count()
                }
            })

class GlobalSearchView(APIView):
    """
    全局搜索接口
    """
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if not query or len(query) < 2:
            return Response({'error': '搜索关键词太短'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 搜索活动
        from apps.activities.models import Activity
        from apps.activities.serializers import ActivitySerializer
        activities = Activity.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )[:5]
        
        # 搜索产品
        from apps.products.models import Product
        from apps.products.serializers import ProductSerializer
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )[:5]
        
        # 搜索文章（如果有文章系统）
        help_articles = HelpArticle.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        ).filter(is_published=True)[:5]
        
        # 搜索用户（仅限管理员）
        users = []
        if request.user.is_authenticated and request.user.is_staff:
            from django.contrib.auth.models import User
            from apps.users.serializers import UserSerializer
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )[:5]
            users = UserSerializer(users, many=True).data
        
        return Response({
            'activities': ActivitySerializer(activities, many=True).data,
            'products': ProductSerializer(products, many=True).data,
            'help_articles': HelpArticleSerializer(help_articles, many=True).data,
            'users': users
        })

class AIAssistantView(APIView):
    """
    AI助手API接口
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessions = {}  # 存储用户会话
        if AI_ASSISTANT_ENABLED:
            try:
                self.app = build_graph()
                logger.info("AI助手流程图构建成功")
            except Exception as e:
                logger.error(f"AI助手流程图构建失败: {str(e)}")
                self.app = None
    
    def get(self, request):
        """检查AI助手状态"""
        if request.path.endswith('/status/'):
            return Response({
                "enabled": AI_ASSISTANT_ENABLED,
                "available": AI_ASSISTANT_ENABLED and self.app is not None,
                "sessions_count": len(self.sessions),
                "user_has_session": request.user.id in self.sessions
            })
        return Response({"error": "不支持的请求"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """处理用户对AI助手的请求"""
        if not AI_ASSISTANT_ENABLED or not self.app:
            # 使用备用AI响应
            user_input = request.data.get('message', '')
            if not user_input:
                return Response({"error": "消息不能为空"}, status=status.HTTP_400_BAD_REQUEST)
                
            response = fallback_ai.respond_to(user_input)
            logger.info(f"使用备用AI响应: '{user_input}' -> '{response}'")
            
            return Response({
                "message": response,
                "session_id": request.user.id,
                "fallback": True
            })
            
        user_id = request.user.id
        user_input = request.data.get('message', '')
        
        if not user_input:
            return Response({"error": "消息不能为空"}, status=status.HTTP_400_BAD_REQUEST)
            
        # 获取或创建用户会话
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                "input": "",
                "output": "",
                "next": "",
                "history": []
            }
        
        # 更新会话状态
        session = self.sessions[user_id]
        session["input"] = user_input
        
        try:
            # 调用AI助手
            logger.info(f"用户 {user_id} 发送消息: {user_input}")
            result = self.app.invoke(session)
            
            # 更新会话历史
            self.sessions[user_id]["history"] = result["history"]
            
            return Response({
                "message": result["output"],
                "session_id": user_id,
                "fallback": False
            })
        except Exception as e:
            logger.error(f"AI处理异常: {str(e)}")
            # 在AI处理异常时也使用备用响应
            response = fallback_ai.respond_to(user_input)
            logger.info(f"异常后使用备用AI响应: '{user_input}' -> '{response}'")
            
            return Response({
                "message": response,
                "session_id": user_id,
                "fallback": True,
                "error": str(e)
            }, status=status.HTTP_200_OK)