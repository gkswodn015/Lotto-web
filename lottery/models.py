# lottery/models.py

from django.db import models
from django.contrib.auth.models import User


class Round(models.Model):
    """추첨 회차"""
    round_number = models.PositiveIntegerField(unique=True)  # 1회차, 2회차...
    draw_date    = models.DateTimeField(null=True, blank=True)
    is_drawn     = models.BooleanField(default=False)  # 추첨 완료 여부

    def __str__(self):
        return f"{self.round_number}회차"


class Ticket(models.Model):
    """구매한 복권 한 장"""
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    round   = models.ForeignKey(Round, on_delete=models.CASCADE)
    # 6개 숫자를 JSON 형태로 저장: [3, 15, 22, 31, 40, 44]
    numbers = models.JSONField()
    is_auto = models.BooleanField(default=False)  # 자동번호 여부
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.pk} ({self.user.username})"


class WinResult(models.Model):
    """당첨 번호 (추첨 결과)"""
    round          = models.OneToOneField(Round, on_delete=models.CASCADE)
    winning_numbers = models.JSONField()   # [3, 15, 22, 31, 40, 44]
    bonus_number   = models.IntegerField() # 보너스 번호
    drawn_at       = models.DateTimeField(auto_now_add=True)


class Prize(models.Model):
    """당첨된 티켓의 등수와 상금"""
    RANK_CHOICES = [(1,'1등'),(2,'2등'),(3,'3등'),(4,'4등'),(5,'5등')]
    round        = models.ForeignKey(Round, on_delete=models.CASCADE)
    ticket       = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    rank         = models.IntegerField(choices=RANK_CHOICES)
    prize_amount = models.DecimalField(max_digits=15, decimal_places=0)
# Create your models here.
