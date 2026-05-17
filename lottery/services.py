# lottery/services.py

import random
from .models import Round, Ticket, WinResult, Prize


def generate_auto_numbers():
    """1~45 중 6개 랜덤 추출, 정렬해서 반환"""
    return sorted(random.sample(range(1, 46), 6))


def determine_rank(matched: int, has_bonus: bool):
    """맞은 개수와 보너스 번호 여부 → 등수 반환 (낙첨이면 None)"""
    if matched == 6:             return 1
    if matched == 5 and has_bonus: return 2
    if matched == 5:             return 3
    if matched == 4:             return 4
    if matched == 3:             return 5
    return None


def perform_draw(round_obj: Round):
    """추첨 실행 — 당첨 번호 생성 후 모든 티켓 등수 계산"""
    if round_obj.is_drawn:
        raise ValueError("이미 추첨된 회차입니다.")

    # 6개 당첨번호 + 보너스 1개 추출
    pool    = list(range(1, 46))
    winning = sorted(random.sample(pool, 6))
    bonus   = random.choice([n for n in pool if n not in winning])

    WinResult.objects.create(
        round=round_obj,
        winning_numbers=winning,
        bonus_number=bonus,
    )

    # 모든 티켓 등수 계산
    prizes = []
    for ticket in Ticket.objects.filter(round=round_obj):
        matched   = len(set(ticket.numbers) & set(winning))
        has_bonus = bonus in ticket.numbers
        rank      = determine_rank(matched, has_bonus)
        if rank:
            amount = {1: 2_000_000_000, 2: 50_000_000,
                      3: 1_500_000, 4: 50_000, 5: 5_000}[rank]
            prizes.append(Prize(
                round=round_obj, ticket=ticket,
                rank=rank, prize_amount=amount
            ))
    Prize.objects.bulk_create(prizes)

    round_obj.is_drawn = True
    round_obj.save()
    return winning, bonus