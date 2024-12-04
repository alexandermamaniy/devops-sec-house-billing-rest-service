import pytest
from buddy_expenses.models import BuddyExpense, ParticipantsOfExpensePayment, PaymentsMadeItByPayers, SettlementByParticipants
from buddy_expenses.serializers import BuddyExpenseSerializer, BuddyExpenseCreateSerializer, SettleParticipantExpenseUpSerializer
from buddy_profiles.models import BuddyProfile
from buddy_groups.models import BuddyGroup
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestBuddyExpenseSerializer:

    def test_create_buddy_expense(self):
        user = User.objects.create_user(email='admin@example.com', password='password123')
        group = BuddyGroup.objects.create(name='Test Group')
        participant = BuddyProfile.objects.create(full_name='Participant', user=user)
        data = {
            'title': 'Test Expense',
            'buddy_group': group.id,
            'description': 'Test Description',
            'total_amount': 100.00,
            'currency': BuddyExpense.Currency.EUR,
            'participants_of_expense_payment': [
                {
                    'participant_id': participant.id,
                    'percentage_to_pay': 50,
                    'amount_to_pay': 50.00,
                    'payment_balance': 0.00
                }
            ]
        }
        context = {'admin': user}
        serializer = BuddyExpenseCreateSerializer(data=data, context=context)
        assert serializer.is_valid()
        buddy_expense = serializer.save()
        assert buddy_expense.title == data['title']
        assert buddy_expense.total_amount == data['total_amount']
        assert buddy_expense.participants_of_expense_payment.count() == 1

    def test_settle_participant_expense(self):
        user = User.objects.create_user(email='admin@example.com', password='password123')
        admin = BuddyProfile.objects.create(full_name='Admin', user=user)
        group = BuddyGroup.objects.create(name='Test Group')
        buddy_expense = BuddyExpense.objects.create(
            title='Test Expense',
            buddy_group=group,
            description='Test Description',
            total_amount=100.00,
            currency=BuddyExpense.Currency.EUR
        )
        data = {
            'who_settle_simple_payment_up': admin.id,
            'what_expense_belong': buddy_expense.id,
            'amount_payment': 50.00
        }
        serializer = SettleParticipantExpenseUpSerializer(data=data)
        assert serializer.is_valid()
        settle_up = serializer.save()
        assert settle_up.amount_payment == data['amount_payment']
        assert settle_up.who_settle_simple_payment_up == admin
        assert settle_up.what_expense_belong == buddy_expense