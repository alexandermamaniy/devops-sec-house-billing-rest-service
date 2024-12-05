import pytest
from django.urls import reverse
from .factories_models_tests import BuddyProfileFactory, BuddyGroupFactory, BuddyExpenseFactory, SettlementByParticipantsFactory
from buddy_expenses.models import BuddyExpense

pytestmark = pytest.mark.django_db

class TestBuddyExpenseCRUD:
    expense_list_create_url = reverse('buddy_expenses:buddy-expenses-create')
    expense_profile_url = reverse('buddy_expenses:buddy-expenses-profile')
    settle_up_participant_url = reverse('buddy_expenses:buddy-expenses-settle-up-participant')

    def test_create_expense(self, api_client):
        group = BuddyGroupFactory()
        data = {
            "title": "Test Expense",
            "buddy_group": group.id,
            "description": "Test Description",
            "total_amount": 100.00,
            "currency": BuddyExpense.Currency.EUR,
            "participants_of_expense_payment": [
                {
                    "participant_id": BuddyProfileFactory().id,
                    "percentage_to_pay": 50,
                    "amount_to_pay": 50.00,
                    "payment_balance": 0.00
                },
                {
                    "participant_id": BuddyProfileFactory().id,
                    "percentage_to_pay": 50,
                    "amount_to_pay": 50.00,
                    "payment_balance": 0.00
                }
            ]
        }
        profile = BuddyProfileFactory()
        user = profile.user
        api_client.force_authenticate(user=user)

        response = api_client.post(self.expense_list_create_url, data, format='json')
        assert response.status_code == 201
        returned_json = response.json()
        assert 'id' in returned_json
        assert returned_json['title'] == data['title']
        assert returned_json['total_amount'] == f"{data['total_amount']:.3f}"

    def test_list_expenses_for_profile(self, api_client):
        profile = BuddyProfileFactory()
        BuddyExpenseFactory.create_batch(5, participants_of_expense_payment=[profile])
        user = profile.user
        api_client.force_authenticate(user=user)

        response = api_client.get(self.expense_profile_url)
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_list_expenses_for_group(self, api_client):
        group = BuddyGroupFactory()
        BuddyExpenseFactory.create_batch(5, buddy_group=group)
        profile = BuddyProfileFactory()
        user = profile.user
        api_client.force_authenticate(user=user)

        url = reverse('buddy_expenses:buddy-expenses-group', args=[group.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_list_settle_up_expenses(self, api_client):
        expense = BuddyExpenseFactory()
        SettlementByParticipantsFactory.create_batch(5, what_expense_belong=expense)
        profile = BuddyProfileFactory()
        user = profile.user
        api_client.force_authenticate(user=user)

        url = reverse('buddy_expenses:buddy-expenses-settle-up', args=[expense.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_create_settle_up_participant(self, api_client):
        expense = BuddyExpenseFactory()
        profile = BuddyProfileFactory()
        user = profile.user
        api_client.force_authenticate(user=user)

        data = {
            "who_settle_simple_payment_up": profile.id,
            "what_expense_belong": expense.id,
            "amount_payment": 50.00
        }

        response = api_client.post(self.settle_up_participant_url, data, format='json')
        assert response.status_code == 201
        returned_json = response.json()
        assert returned_json['amount_payment'] == f"{data['amount_payment']:.3f}"