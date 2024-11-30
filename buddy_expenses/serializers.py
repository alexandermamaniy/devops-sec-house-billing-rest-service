from rest_framework import serializers

from buddy_expenses.models import BuddyExpense, PaymentsMadeItByPayers, SettlementByParticipants, ParticipantsOfExpensePayment
from buddy_groups.admin import buddy_members_inline
from buddy_profiles.models import BuddyProfile

class PayerPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentsMadeItByPayers
        fields = ['who_do_simple_payment', 'amount_payment']

class SettleParticipantExpenseUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettlementByParticipants
        fields = ['who_settle_simple_payment_up', 'amount_payment']

class ParticipantsOfExpensePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantsOfExpensePayment
        fields = ['participant_id', 'percentage_to_pay', 'amount_to_pay', 'payment_balance']


class BuddyExpenseSerializer(serializers.ModelSerializer):
    participants_of_expense_payment = ParticipantsOfExpensePaymentSerializer(source='participantsofexpensepayment_set', many=True, read_only=False)
    payments_made_it_by_payers = PayerPaymentsSerializer(source='paymentsmadeitbypayers_set', many=True, read_only=False)
    settlement_by_participants = SettleParticipantExpenseUpSerializer(source='settlementbyparticipants_set', many=True, read_only=False)

    class Meta:
        model = BuddyExpense
        fields = [
            'id', 'title', 'buddy_group', 'description', 'total_amount',
            'currency', 'type_payment_distribution', 'evicende_picture_url',
            'payments_made_it_by_payers', 'settlement_by_participants', 'participants_of_expense_payment', 'created_date'
        ]

    def create(self, validated_data):
        payments_made_it_by_payers_data = validated_data.pop('paymentsmadeitbypayers_set', [])
        settlement_by_participants_data = validated_data.pop('settlementbyparticipants_set', [])
        participants_of_expense_payment_data = validated_data.pop('participantsofexpensepayment_set', [])

        buddy_expense = BuddyExpense.objects.create(**validated_data)

        for payer_data in payments_made_it_by_payers_data:
            PaymentsMadeItByPayers.objects.create(
                what_expense_belong_to=buddy_expense,
                who_do_simple_payment=payer_data['who_do_simple_payment'],
                amount_payment=payer_data['amount_payment']
            )

        for participant_data in settlement_by_participants_data:
            SettlementByParticipants.objects.create(
                what_expense_belong=buddy_expense,
                who_settle_simple_payment_up=participant_data['who_settle_simple_payment_up'],
                amount_payment=participant_data['amount_payment']
            )

        for participant_of_expense_payment_data in participants_of_expense_payment_data:
            ParticipantsOfExpensePayment.objects.create(
                expense=buddy_expense,
                participant_id=participant_of_expense_payment_data['participant_id'],
                percentage_to_pay=participant_of_expense_payment_data['percentage_to_pay'],
                amount_to_pay=participant_of_expense_payment_data['amount_to_pay'],
                payment_balance=participant_of_expense_payment_data['payment_balance']
            )
        return buddy_expense

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.paymentsmadeitbypayers_set = validated_data.get('payments_made_it_by_payers', instance.paymentsmadeitbypayers_set)
    #     instance.settleparticipantexpenseup_set = validated_data.get('settlement_by_participants', instance.settleparticipantexpenseup_set)
    #     instance.participantsofexpensepayment_set = validated_data.get('participants_of_expense_payment', instance.participantsofexpensepayment_set)
    #     instance.save()
    #
    #     return  instance



class BuddyExpenseCreateSerializer(serializers.ModelSerializer):
    participants_of_expense_payment = ParticipantsOfExpensePaymentSerializer(source='participantsofexpensepayment_set',
                                                                             many=True, read_only=False)

    class Meta:
        model = BuddyExpense
        fields = [
            'id', 'title', 'buddy_group', 'description', 'total_amount',
            'currency', 'participants_of_expense_payment'
        ]

    def create(self, validated_data):
        participants_of_expense_payment_data = validated_data.pop('participantsofexpensepayment_set', [])

        buddy_expense = BuddyExpense.objects.create(**validated_data)

        group_admin = self.context.get('admin')
        buddy_profile_admin = BuddyProfile.objects.get(user=group_admin)


        PaymentsMadeItByPayers.objects.create(
            what_expense_belong_to=buddy_expense,
            who_do_simple_payment=buddy_profile_admin,
            amount_payment=validated_data.pop('total_amount'))


        for participant_of_expense_payment_data in participants_of_expense_payment_data:
            ParticipantsOfExpensePayment.objects.create(
                expense=buddy_expense,
                participant_id=participant_of_expense_payment_data['participant_id'],
                percentage_to_pay=participant_of_expense_payment_data['percentage_to_pay'],
                amount_to_pay=participant_of_expense_payment_data['amount_to_pay'],
                payment_balance=participant_of_expense_payment_data['payment_balance']
            )
        return buddy_expense
