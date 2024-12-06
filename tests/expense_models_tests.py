import pytest
from buddy_expenses.models import BuddyExpense, ParticipantsOfExpensePayment, PaymentsMadeItByPayers, SettlementByParticipants
from buddy_profiles.models import BuddyProfile
from buddy_groups.models import BuddyGroup
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()

@pytest.mark.django_db
class TestBuddyExpenseModel:


    def test_create_buddy_expense(self):
        group = BuddyGroup.objects.create(name='Test Group')
        buddy_expense = BuddyExpense.objects.create(
            title='Test Expense',
            buddy_group=group,
            description='Test Description',
            total_amount=100.00,
            currency=BuddyExpense.Currency.EUR
        )
        assert buddy_expense.title == 'Test Expense'
        assert buddy_expense.total_amount == 100.00

    def test_add_participant_to_expense(self):
        self.fake_email = fake.email()
        self.fake_participant_password = fake.password()

        user = User.objects.create_user(email=self.fake_email, password=self.fake_participant_password)
        participant = BuddyProfile.objects.create(full_name='Participant', user=user)
        group = BuddyGroup.objects.create(name='Test Group')
        buddy_expense = BuddyExpense.objects.create(
            title='Test Expense',
            buddy_group=group,
            description='Test Description',
            total_amount=100.00,
            currency=BuddyExpense.Currency.EUR
        )
        ParticipantsOfExpensePayment.objects.create(
            expense=buddy_expense,
            participant_id=participant,
            percentage_to_pay=50,
            amount_to_pay=50.00,
            payment_balance=0.00
        )
        assert buddy_expense.participants_of_expense_payment.count() == 1

    def test_add_payment_to_expense(self):
        self.fake_email = fake.email()
        self.fake_payer_password = fake.password()
        user = User.objects.create_user(email=self.fake_email, password=self.fake_payer_password)
        payer = BuddyProfile.objects.create(full_name='Payer', user=user)
        group = BuddyGroup.objects.create(name='Test Group')
        buddy_expense = BuddyExpense.objects.create(
            title='Test Expense',
            buddy_group=group,
            description='Test Description',
            total_amount=100.00,
            currency=BuddyExpense.Currency.EUR
        )
        PaymentsMadeItByPayers.objects.create(
            what_expense_belong_to=buddy_expense,
            who_do_simple_payment=payer,
            amount_payment=50.00
        )
        assert buddy_expense.payments_made_it_by_payers.count() == 1

    def test_settle_participant_expense(self):
        self.fake_email= fake.email()
        self.fake_settlet_password = fake.password()
        user = User.objects.create_user(email=self.fake_email, password=self.fake_settlet_password)
        settler = BuddyProfile.objects.create(full_name='Settler', user=user)
        group = BuddyGroup.objects.create(name='Test Group')
        buddy_expense = BuddyExpense.objects.create(
            title='Test Expense',
            buddy_group=group,
            description='Test Description',
            total_amount=100.00,
            currency=BuddyExpense.Currency.EUR
        )
        SettlementByParticipants.objects.create(
            who_settle_simple_payment_up=settler,
            what_expense_belong=buddy_expense,
            amount_payment=50.00
        )
        assert buddy_expense.settlement_by_participants.count() == 1