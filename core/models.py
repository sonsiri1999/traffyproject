from django.db import models

# Create your models here.
# core/models.py

from django.db import models
from django.contrib.auth.models import User

# โมเดลสำหรับเรื่องร้องเรียน
class Case(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('in_progress', 'กำลังดำเนินการ'),
        ('resolved', 'แก้ไขแล้ว'),
    ]

    CATEGORY_CHOICES = [
        ('electrical', 'ไฟฟ้า'),
        ('water_supply', 'ประปา'),
        ('road_damage', 'ถนน/ทางเท้า'),
        ('other', 'อื่นๆ'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_cases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # เพิ่มฟิลด์สำหรับรูปภาพ
    image_file = models.ImageField(upload_to='case_images/', blank=True, null=True)

    def __str__(self):
        return self.title

# โมเดลสำหรับแนบรูปภาพ
class Image(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='case_images/')

    def __str__(self):
        return f"รูปภาพของเรื่อง: {self.case.title}"

# โมเดลสำหรับผู้ติดตาม
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_cases')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'case')

    def __str__(self):
        return f"{self.user.username} ติดตามเรื่อง: {self.case.title}"

class Comment(models.Model):
    case = models.ForeignKey(
        Case, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    image_file = models.ImageField(
        upload_to='comment_images/', 
        blank=True, 
        null=True
    ) # เพิ่มบรรทัดนี้
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.case.title}'