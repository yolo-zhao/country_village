# backend/apps/activities/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ActivityReview, ActivityComment, ActivityLike, Activity
from django.conf import settings
from openai import OpenAI
from django.contrib.contenttypes.models import ContentType

DEEPSEEK_API_KEY = getattr(settings, 'DEEPSEEK_API_KEY', None)
DEEPSEEK_API_BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_BASE_URL)

def call_deepseek_api(prompt):
    if DEEPSEEK_API_KEY and DEEPSEEK_API_BASE_URL:
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"调用 DeepSeek API 失败: {e}")
            return ""
    else:
        print("DeepSeek API 密钥或 URL 未配置")
        return ""

@receiver(post_save, sender=ActivityReview)
def automatically_reply_to_review(sender, instance, created, **kwargs):
    if created and DEEPSEEK_API_KEY:
        review_text = instance.comment
        review_rating = instance.rating
        activity = instance.activity
        like_count = ActivityLike.objects.filter(content_type=ContentType.objects.get_for_model(ActivityReview), object_id=instance.id).count()

        if review_rating <= 2:
            prompt = f"用户对活动 '{activity.title}' 的评价是：'{review_text}'。这条评价获得了 {like_count} 个点赞。请生成一段更重视的道歉回复。"
        elif review_rating >= 4:
            prompt = f"用户对活动 '{activity.title}' 的评价是：'{review_text}'。这条评价获得了 {like_count} 个点赞。请生成一段更热情的感谢回复。"
        else:
            prompt = f"用户对活动 '{activity.title}' 的评价是：'{review_text}'。这条评价获得了 {like_count} 个点赞。请生成一段通用回复。"

        auto_reply = call_deepseek_api(prompt)
        farmer_name = activity.farmer.get_full_name() or activity.farmer.username  # 移动到这里

        if auto_reply:
            instance.auto_reply = f"{auto_reply}\n\n活动主办方：{farmer_name} 敬上"
            instance.save(update_fields=['auto_reply'])


@receiver(post_save, sender=ActivityComment)
def automatically_reply_to_comment(sender, instance, created, **kwargs):
    if created and DEEPSEEK_API_KEY:
        comment_text = instance.text
        activity = None
        if instance.content_type.model == 'activity':
            try:
                activity = Activity.objects.get(pk=instance.object_id)
            except Activity.DoesNotExist:
                return
        elif instance.content_type.model == 'activityreview':
            try:
                activity_review = ActivityReview.objects.get(pk=instance.object_id)
                activity = activity_review.activity
            except ActivityReview.DoesNotExist:
                return

        if activity:
            like_count = ActivityLike.objects.filter(content_type=instance.content_type,
                                                     object_id=instance.object_id).count()
            prompt = f"用户对活动 '{activity.title}' 的评论是：'{comment_text}'。这条评论获得了 {like_count} 个点赞。请生成一段礼貌的回应。"
            auto_reply = call_deepseek_api(prompt)
            farmer_name = activity.farmer.get_full_name() or activity.farmer.username  # 移动到这里
            if auto_reply:
                instance.auto_reply = f"{auto_reply}\n\n活动主办方：{farmer_name} 敬上"
                instance.save(update_fields=['auto_reply'])


@receiver(post_save, sender=ActivityLike)
def handle_activity_like(sender, instance, created, **kwargs):
    if created and DEEPSEEK_API_KEY:
        content_type = instance.content_type
        object_id = instance.object_id

        if content_type.model == 'activity':
            try:
                activity = Activity.objects.get(pk=object_id)
                like_count = ActivityLike.objects.filter(content_type=content_type, object_id=object_id).count()
                if like_count >= 10:
                    prompt = f"您的活动 '{activity.title}' 收到了 {like_count} 个点赞。请生成一句感谢大家支持的简短回复。"
                    auto_reply = call_deepseek_api(prompt)
                    if auto_reply:
                        print(f"活动 '{activity.title}' 自动回复: {auto_reply}")
            except Activity.DoesNotExist:
                print(f"找不到 ID 为 {object_id} 的活动。")

        elif content_type.model == 'activityreview':
            try:
                review = ActivityReview.objects.get(pk=object_id)
                like_count = ActivityLike.objects.filter(content_type=content_type, object_id=object_id).count()
                print(f"评价 '{review.comment[:50]}...' 收到了 {like_count} 个点赞。")
            except ActivityReview.DoesNotExist:
                print(f"找不到 ID 为 {object_id} 的评价。")

        elif content_type.model == 'activitycomment':
            try:
                comment = ActivityComment.objects.get(pk=object_id)
                like_count = ActivityLike.objects.filter(content_type=content_type, object_id=object_id).count()
                print(f"评论 '{comment.text[:50]}...' 收到了 {like_count} 个点赞。")
            except ActivityComment.DoesNotExist:
                print(f"找不到 ID 为 {object_id} 的评论。")