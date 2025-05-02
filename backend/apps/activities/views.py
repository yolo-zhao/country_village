# backend/apps/activities/views.py
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import timedelta
import calendar
import math
from django.contrib.contenttypes.models import ContentType
from .models import ActivityCategory, Tag, Activity, ActivityImage, Reservation, ActivityReview, ActivityPhoto, ActivityCheckIn, ActivityLike, ActivityComment
from .serializers import ActivityCategorySerializer, TagSerializer, ActivitySerializer, ActivityImageSerializer, ReservationSerializer, ActivityReviewSerializer, ActivityPhotoSerializer, ActivityCheckInSerializer, ActivityLikeSerializer, ActivityCommentSerializer
from rest_framework import serializers
from rest_framework import status

class ActivityCategoryViewSet(viewsets.ModelViewSet):
    queryset = ActivityCategory.objects.all()
    serializer_class = ActivityCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # 获取并处理分类ID
        category_id = self.request.data.get('category_id')
        if not category_id and 'category' in self.request.data:
            category_id = self.request.data.get('category')
        
        # 调试日志
        print(f"创建活动，接收到的分类ID: {category_id}, 类型: {type(category_id)}")
        
        try:
            # 尝试获取分类对象
            if category_id:
                category = ActivityCategory.objects.get(id=category_id)
                serializer.save(farmer=self.request.user, category=category)
            else:
                # 如果没有分类ID，将引发验证错误
                serializer.save(farmer=self.request.user)
        except ActivityCategory.DoesNotExist:
            # 分类不存在
            raise serializers.ValidationError({"category": f"ID为{category_id}的活动分类不存在"})
        except Exception as e:
            # 其他异常
            print(f"创建活动时发生错误: {str(e)}")
            raise

    def update(self, request, *args, **kwargs):
        # 调试日志
        print(f"更新活动，接收到的数据: {request.data}")
        
        # 获取并处理分类ID
        category_id = request.data.get('category_id')
        if not category_id and 'category' in request.data:
            category_id = request.data.get('category')
            
        # 确保category_id是有效的
        if category_id:
            try:
                # 验证分类ID存在
                ActivityCategory.objects.get(id=category_id)
            except ActivityCategory.DoesNotExist:
                return Response(
                    {"category": f"ID为{category_id}的活动分类不存在"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().update(request, *args, **kwargs)

class ActivityImageViewSet(viewsets.ModelViewSet):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能管理自己的预约

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 获取请求中的活动ID
        activity_id = self.request.data.get('activity')
        # 如果没有直接提供，可能是API需要从URL中获取
        if not activity_id and 'activity_id' in self.request.data:
            activity_id = self.request.data.get('activity_id')
            
        # 确保有活动ID
        if not activity_id:
            raise serializers.ValidationError({"activity": "活动ID不能为空"})
            
        try:
            # 获取活动对象
            activity = Activity.objects.get(id=activity_id)
            # 保存预约，设置用户和活动
            serializer.save(user=self.request.user, activity=activity)
        except Activity.DoesNotExist:
            raise serializers.ValidationError({"activity": "指定的活动不存在"})

class ActivityReviewViewSet(viewsets.ModelViewSet):
    queryset = ActivityReview.objects.all()
    serializer_class = ActivityReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityPhotoViewSet(viewsets.ModelViewSet):
    queryset = ActivityPhoto.objects.all()
    serializer_class = ActivityPhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityCheckInViewSet(viewsets.ModelViewSet):
    queryset = ActivityCheckIn.objects.all()
    serializer_class = ActivityCheckInSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能创建打卡记录

    def get_queryset(self):
        return ActivityCheckIn.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityLikeViewSet(viewsets.ModelViewSet):
    queryset = ActivityLike.objects.all()
    serializer_class = ActivityLikeSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能点赞

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityCommentViewSet(viewsets.ModelViewSet):
    queryset = ActivityComment.objects.all()
    serializer_class = ActivityCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 新增的视图类

class UserActivitiesView(APIView):
    """
    获取当前用户参与的活动
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 获取用户的所有预约
        reservations = Reservation.objects.filter(user=request.user)
        
        # 获取用户的所有打卡记录
        check_ins = ActivityCheckIn.objects.filter(user=request.user)
        
        # 整合活动ID
        activity_ids = list(reservations.values_list('activity_id', flat=True))
        activity_ids.extend(check_ins.values_list('activity_id', flat=True))
        activity_ids = list(set(activity_ids))  # 去重
        
        # 查询活动详情
        activities = Activity.objects.filter(id__in=activity_ids)
        
        # 添加额外信息
        result = []
        for activity in activities:
            activity_data = ActivitySerializer(activity).data
            
            # 添加参与状态
            activity_data['status'] = 'pending'  # 默认状态
            
            # 检查是否有预约
            user_reservations = reservations.filter(activity=activity)
            if user_reservations.exists():
                reservation = user_reservations.first()
                activity_data['reservation_id'] = reservation.id
                activity_data['reservation_status'] = reservation.status
                activity_data['reservation_date'] = reservation.reservation_date
            
            # 检查是否有打卡记录
            user_check_ins = check_ins.filter(activity=activity)
            if user_check_ins.exists():
                check_in = user_check_ins.first()
                activity_data['checked_in'] = True
                activity_data['check_in_time'] = check_in.check_in_time
                activity_data['status'] = 'completed'
            else:
                activity_data['checked_in'] = False
            
            result.append(activity_data)
        
        # 计算总数
        total_count = len(result)
        
        return Response({
            'count': total_count,
            'results': result
        })

class ActivitySearchView(generics.ListAPIView):
    """
    活动搜索视图
    """
    serializer_class = ActivitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'location']
    
    def get_queryset(self):
        queryset = Activity.objects.all()
        
        # 分类过滤
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 标签过滤
        tag_id = self.request.query_params.get('tag', None)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        
        # 日期范围过滤
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            queryset = queryset.filter(end_time__lte=end_date)
        
        # 价格范围过滤（如果有价格字段）
        # min_price = self.request.query_params.get('min_price', None)
        # if min_price:
        #     queryset = queryset.filter(price__gte=min_price)
        
        # max_price = self.request.query_params.get('max_price', None)
        # if max_price:
        #     queryset = queryset.filter(price__lte=max_price)
        
        return queryset

class ActivityRecommendationsView(APIView):
    """
    活动推荐视图
    """
    def get(self, request):
        # 获取用户感兴趣的分类和标签
        user_categories = set()
        user_tags = set()
        
        if request.user.is_authenticated:
            # 获取用户之前参与的活动
            user_reservations = Reservation.objects.filter(user=request.user)
            user_check_ins = ActivityCheckIn.objects.filter(user=request.user)
            
            # 提取分类和标签
            user_activity_ids = list(user_reservations.values_list('activity_id', flat=True))
            user_activity_ids.extend(user_check_ins.values_list('activity_id', flat=True))
            
            if user_activity_ids:
                user_activities = Activity.objects.filter(id__in=user_activity_ids)
                user_categories = set(user_activities.values_list('category_id', flat=True))
                
                # 获取用户活动的所有标签
                for activity in user_activities:
                    user_tags.update(activity.tags.values_list('id', flat=True))
        
        # 推荐基于用户兴趣的活动
        recommended_activities = []
        
        # 1. 首先推荐基于用户兴趣的活动
        if user_categories or user_tags:
            interest_activities = Activity.objects.filter(
                Q(category_id__in=user_categories) | Q(tags__id__in=user_tags)
            ).distinct()
            
            # 排除用户已经参与过的活动
            if request.user.is_authenticated:
                interest_activities = interest_activities.exclude(id__in=user_activity_ids)
            
            recommended_activities.extend(interest_activities[:5])  # 最多推荐5个基于兴趣的活动
        
        # 2. 推荐热门活动（根据预约和打卡数量）
        popular_activities = Activity.objects.annotate(
            reservation_count=Count('reservations'),
            check_in_count=Count('check_ins')
        ).order_by('-reservation_count', '-check_in_count')
        
        # 排除已经推荐的活动
        popular_activities = popular_activities.exclude(id__in=[a.id for a in recommended_activities])
        
        # 将热门活动添加到推荐列表中
        recommended_activities.extend(popular_activities[:5])  # 最多推荐5个热门活动
        
        # 3. 推荐即将开始的活动
        now = timezone.now()
        upcoming_activities = Activity.objects.filter(
            start_time__gt=now,
            start_time__lt=now + timedelta(days=7)  # 未来一周内的活动
        ).order_by('start_time')
        
        # 排除已经推荐的活动
        upcoming_activities = upcoming_activities.exclude(id__in=[a.id for a in recommended_activities])
        
        # 将即将开始的活动添加到推荐列表中
        recommended_activities.extend(upcoming_activities[:5])  # 最多推荐5个即将开始的活动
        
        # 确保不超过10个推荐
        recommended_activities = recommended_activities[:10]
        
        # 序列化返回
        serializer = ActivitySerializer(recommended_activities, many=True)
        return Response(serializer.data)

class ActivityStatisticsView(APIView):
    """
    活动统计数据视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # 只允许农户或管理员访问详细统计数据
        if not (hasattr(request.user, 'farmerprofile') or request.user.is_staff):
            return Response({"error": "只有农户或管理员可以访问活动统计数据"}, status=403)
        
        # 获取特定活动统计数据
        activity_id = request.query_params.get('activity_id', None)
        
        if activity_id:
            try:
                activity = Activity.objects.get(id=activity_id)
                
                # 验证权限：只有活动的创建者或管理员可以查看详细统计数据
                if activity.farmer != request.user and not request.user.is_staff:
                    return Response({"error": "您没有权限查看此活动的统计数据"}, status=403)
                
                # 统计预约数据
                reservations = Reservation.objects.filter(activity=activity)
                reservations_count = reservations.count()
                reservations_by_status = reservations.values('status').annotate(count=Count('status'))
                
                # 统计打卡数据
                check_ins_count = ActivityCheckIn.objects.filter(activity=activity).count()
                
                # 统计评价数据
                reviews = ActivityReview.objects.filter(activity=activity)
                reviews_count = reviews.count()
                avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
                
                # 统计点赞评论数据
                content_type_id = ContentType.objects.get_for_model(Activity).id
                likes_count = ActivityLike.objects.filter(
                    content_type_id=content_type_id,
                    object_id=activity.id
                ).count()
                
                comments_count = ActivityComment.objects.filter(
                    content_type_id=content_type_id,
                    object_id=activity.id
                ).count()
                
                return Response({
                    'activity_id': activity.id,
                    'title': activity.title,
                    'reservations': {
                        'total': reservations_count,
                        'by_status': reservations_by_status
                    },
                    'check_ins': check_ins_count,
                    'completion_rate': (check_ins_count / reservations_count) * 100 if reservations_count > 0 else 0,
                    'reviews': {
                        'count': reviews_count,
                        'average_rating': avg_rating
                    },
                    'engagement': {
                        'likes': likes_count,
                        'comments': comments_count
                    }
                })
                
            except Activity.DoesNotExist:
                return Response({"error": "活动不存在"}, status=404)
                
        else:
            # 农户只能查看自己创建的活动的统计数据
            if hasattr(request.user, 'farmerprofile'):
                activities = Activity.objects.filter(farmer=request.user)
            else:  # 管理员可以查看所有活动的统计数据
                activities = Activity.objects.all()
            
            # 统计活动数量
            total_activities = activities.count()
            
            # 按分类统计活动数量
            activities_by_category = activities.values('category__name').annotate(count=Count('id'))
            
            # 统计预约总数和状态分布
            total_reservations = Reservation.objects.filter(activity__in=activities).count()
            reservations_by_status = Reservation.objects.filter(activity__in=activities).values('status').annotate(count=Count('status'))
            
            # 统计打卡总数
            total_check_ins = ActivityCheckIn.objects.filter(activity__in=activities).count()
            
            # 统计最热门的活动（基于预约数）
            popular_activities = Activity.objects.filter(id__in=activities).annotate(
                reservation_count=Count('reservations')
            ).order_by('-reservation_count')[:5]
            
            popular_activities_data = [{
                'id': activity.id,
                'title': activity.title,
                'reservations': activity.reservation_count
            } for activity in popular_activities]
            
            return Response({
                'total_activities': total_activities,
                'activities_by_category': activities_by_category,
                'reservations': {
                    'total': total_reservations,
                    'by_status': reservations_by_status
                },
                'check_ins': total_check_ins,
                'popular_activities': popular_activities_data
            })

class NearbyActivitiesView(APIView):
    """
    附近活动视图
    """
    def get(self, request):
        # 从请求参数中获取当前位置
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        
        # 默认搜索半径（单位：公里）
        radius = float(request.query_params.get('radius', 10))
        
        if not latitude or not longitude:
            return Response({"error": "需要提供位置信息 (latitude, longitude)"}, status=400)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response({"error": "位置信息格式不正确"}, status=400)
        
        # 使用自定义的距离计算而不是 GeoDjango
        # 使用 Haversine 公式计算两点之间的距离
        def calculate_distance(lat1, lon1, lat2, lon2):
            # 地球半径（公里）
            R = 6371.0
            
            # 将经纬度转换为弧度
            lat1_rad = math.radians(lat1)
            lon1_rad = math.radians(lon1)
            lat2_rad = math.radians(lat2)
            lon2_rad = math.radians(lon2)
            
            # 经纬度差值
            dlon = lon2_rad - lon1_rad
            dlat = lat2_rad - lat1_rad
            
            # Haversine 公式
            a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c
            
            return distance
        
        # 获取所有活动
        all_activities = Activity.objects.all()
        
        # 计算每个活动与用户位置的距离
        nearby_activities = []
        for activity in all_activities:
            # 跳过没有位置信息的活动
            if activity.location_latitude is None or activity.location_longitude is None:
                continue
            
            # 计算距离
            distance = calculate_distance(
                latitude, longitude, 
                activity.location_latitude, activity.location_longitude
            )
            
            # 如果在指定半径内，添加到结果列表
            if distance <= radius:
                # 添加距离信息到活动对象
                activity_data = ActivitySerializer(activity).data
                activity_data['distance'] = round(distance, 2)  # 四舍五入到2位小数
                nearby_activities.append(activity_data)
        
        # 按距离排序
        nearby_activities.sort(key=lambda x: x['distance'])
        
        return Response(nearby_activities)

class PopularActivitiesView(APIView):
    """
    热门活动视图
    """
    def get(self, request):
        # 计算时间范围（默认为过去30天）
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # 统计活动的预约数、打卡数、评价数、点赞数和评论数
        activities = Activity.objects.filter(
            Q(start_time__gte=start_date) | Q(end_time__gte=start_date)
        ).annotate(
            reservations_count=Count('reservations', distinct=True),
            check_ins_count=Count('check_ins', distinct=True),
            reviews_count=Count('reviews', distinct=True)
            # 注意：因为点赞和评论使用的是通用外键，这里的计算会比较复杂
        ).order_by('-reservations_count', '-check_ins_count', '-reviews_count')[:10]
        
        # 序列化结果
        serializer = ActivitySerializer(activities, many=True)
        result = serializer.data
        
        # 为每个活动添加流行度指标
        for i, activity in enumerate(activities):
            result[i]['popularity'] = {
                'reservations': activity.reservations_count,
                'check_ins': activity.check_ins_count,
                'reviews': activity.reviews_count
            }
        
        return Response(result)

class ActivityCalendarView(APIView):
    """
    活动日历视图
    """
    def get(self, request):
        # 获取年月参数，默认为当前年月
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        # 计算月份的第一天和最后一天
        first_day = timezone.datetime(year, month, 1)
        last_day = timezone.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        
        # 查询指定月份的活动
        month_activities = Activity.objects.filter(
            Q(start_time__gte=first_day, start_time__lte=last_day) |  # 活动开始时间在当月
            Q(end_time__gte=first_day, end_time__lte=last_day) |  # 活动结束时间在当月
            Q(start_time__lte=first_day, end_time__gte=last_day)  # 活动跨越整个月份
        ).order_by('start_time')
        
        # 按日期组织活动
        calendar_data = {}
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            current_date = timezone.datetime(year, month, day)
            next_date = current_date + timedelta(days=1)
            
            # 查找当天的活动
            day_activities = month_activities.filter(
                Q(start_time__gte=current_date, start_time__lt=next_date) |  # 当天开始的活动
                Q(start_time__lt=current_date, end_time__gte=current_date)  # 跨越当天的活动
            )
            
            # 如果当天有活动，则添加到日历数据中
            if day_activities.exists():
                calendar_data[str(day)] = ActivitySerializer(day_activities, many=True).data
        
        return Response({
            'year': year,
            'month': month,
            'activities': calendar_data
        })

class ActivityReservationViewSet(viewsets.ModelViewSet):
    """
    处理特定活动的预约
    通过 /activities/{activity_id}/reservations/ 路径访问
    """
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 获取URL中的活动ID
        activity_id = self.kwargs.get('activity_pk')
        # 根据用户角色决定可见范围
        user = self.request.user
        
        # 如果是活动创建者（农户），可以查看所有该活动的预约
        activity = Activity.objects.get(id=activity_id)
        if activity.farmer == user:
            return Reservation.objects.filter(activity_id=activity_id)
        
        # 普通用户只能查看自己的预约
        return Reservation.objects.filter(
            activity_id=activity_id,
            user=user
        )
    
    def perform_create(self, serializer):
        # 从URL获取活动ID
        activity_id = self.kwargs.get('activity_pk')
        try:
            # 获取活动对象
            activity = Activity.objects.get(id=activity_id)
            # 保存预约，设置用户和活动
            serializer.save(user=self.request.user, activity=activity)
        except Activity.DoesNotExist:
            raise serializers.ValidationError({"activity": "指定的活动不存在"})