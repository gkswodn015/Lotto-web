# Create your views here.
# admin_panel/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from lottery.models import Round, Ticket, Prize
from lottery.services import perform_draw


@staff_member_required
def sales_view(request):
    rounds  = Round.objects.all()
    sel     = request.GET.get('round')
    tickets = Ticket.objects.select_related('user', 'round').order_by('-purchased_at')
    if sel:
        tickets = tickets.filter(round__round_number=sel)
    return render(request, 'admin_panel/sales.html', {
        'rounds': rounds, 'tickets': tickets, 'selected': sel
    })


@staff_member_required
def draw_view(request):
    pending = Round.objects.filter(is_drawn=False).order_by('round_number')
    if request.method == 'POST':
        round_id = request.POST.get('round_id')
        try:
            round_obj = Round.objects.get(pk=round_id)
            winning, bonus = perform_draw(round_obj)
            messages.success(request,
                f'✅ 추첨 완료! 당첨번호: {winning}  보너스: {bonus}')
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('admin_panel:draw')
    return render(request, 'admin_panel/draw.html', {'pending_rounds': pending})


@staff_member_required
def winners_view(request):
    prizes = Prize.objects.select_related(
        'ticket__user', 'round'
    ).order_by('round__round_number', 'rank')
    return render(request, 'admin_panel/winners.html', {'prizes': prizes})