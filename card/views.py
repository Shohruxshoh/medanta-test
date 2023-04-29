import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views import View
from service.models import PayInstallmentPeriod, Debts
from card.models import CardUser


# Create your views here.

class CreateCardView(LoginRequiredMixin, CreateView):
    model = CardUser
    template_name = 'card/create_card.html'
    fields = ['user', 'card_number', 'card_mm', 'card_yy']
    success_url = '/'


CARD_MONEY = 330000


class DebtsCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pay_installment_results = PayInstallmentPeriod.objects.filter().exclude(is_paid=True)
        for pay_installment_result in pay_installment_results:
            if pay_installment_result.sum == CARD_MONEY:
                pay_installment_result.is_paid = True
                pay_installment_result.pay_date = datetime.datetime.now()
                pay_installment_result.save()
            else:
                create_debit = Debts.objects.create(pay_installment_period=pay_installment_result)
            debit_results = Debts.objects.filter(pay_installment_period=pay_installment_result)
            if debit_result > 0:
                for debit_result in debit_results:
                    debit += debit_result.pay_installment_period.sum
                    if debit == CARD_MONEY:
                        pay_installment_result.is_paid = True
                        pay_installment_result.pay_date = datetime.datetime.now()
                        debit_result.amount_received = CARD_MONEY
                        debit_result.save()
                        pay_installment_result.save()
                    else:
                        # curl = CARD_MONEY/2
                        if curl == '200':
                            debit_result.amount_received = CARD_MONEY / 2
                            debit_result.save()

        return render(request, 'abs.html')
    # Ruchnoy
    # Debits.objects.filter()
    # #cron
    #
    # installMent_results = Installment.objests.filter(month).exclude(is_paid)
    # for installMent_result in installMent_results:
    #     debit_result = Debits.objects.filter(start == datetime.monht, installment=installMent_ result)
    #     if debit_result >0:
    #         qarz += debit_result.sum
    #         qarzdorlik
    #     if(qarzdorlik == CARD_MONEY):
    #         is_paid = True
    #     else:
    #         curl = CARD_MONEY / 2
    #         if curl == '200'
    #             Debits.object.create =
    #         else:
    #             curl = CARD_MONEY / 2
    #             curl = CARD_MONEY / 4
    #             curl = CARD_MONEY / 6
    #             curl = CARD_MONEY / 10
