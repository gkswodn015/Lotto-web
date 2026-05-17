# lottery/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Round, Ticket
from .services import generate_auto_numbers

@login_required  # 로그인 안 하면 로그인 페이지로 보냄
def buy_ticket(request):
    # 아직 추첨 안 된 가장 최근 회차 가져오기
    current_round = Round.objects.filter(is_drawn=False).first()
    if not current_round:
        messages.error(request, "현재 진행 중인 회차가 없습니다.")
        return redirect('lottery:my_tickets')

    if request.method == 'POST':
        mode = request.POST.get('mode')  # 'auto' 또는 'manual'

        if mode == 'auto':
            numbers = generate_auto_numbers()
        else:
            # 체크박스로 받은 숫자들
            raw = request.POST.getlist('number')
            numbers = sorted([int(n) for n in raw if n.isdigit()])
            # 유효성 검사
            if len(numbers) != 6 or len(set(numbers)) != 6:
                messages.error(request, "1~45 중 중복 없이 6개를 선택하세요.")
                return redirect('lottery:buy')
            if not all(1 <= n <= 45 for n in numbers):
                messages.error(request, "번호는 1~45 사이여야 합니다.")
                return redirect('lottery:buy')

        Ticket.objects.create(
            user=request.user,
            round=current_round,
            numbers=numbers,
            is_auto=(mode == 'auto'),
        )
        messages.success(request, f"구매 완료! 번호: {numbers}")
        return redirect('lottery:my_tickets')

    # GET: 구매 폼 보여주기
    return render(request, 'lottery/buy.html', {
        'round': current_round,
        'number_range': range(1, 46),  # 템플릿에서 1~45 번호 그리드 그릴 때 사용
    })


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(
        user=request.user
    ).select_related('round').order_by('-purchased_at')
    return render(request, 'lottery/my_tickets.html', {'tickets': tickets})
