import factory
from faker import Faker

from buddy_expenses.models import BuddyExpense, ParticipantsOfExpensePayment, PaymentsMadeItByPayers, \
    SettlementByParticipants
from buddy_groups.models import BuddyGroup, GroupMembers, GroupAdmins
from buddy_profiles.models import BuddyProfile
from users.models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = fake.password()
    is_staff = False
    is_superuser = False

class BuddyProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuddyProfile

    user = factory.SubFactory(UserFactory)
    full_name = fake.name()
    picture_url = fake.image_url()


class BuddyGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuddyGroup

    name = fake.name()

    @factory.post_generation
    def group_members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                GroupMembers.objects.create(group_belong_to=self, buddy_profile_member=member)

    @factory.post_generation
    def group_admins(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for admin in extracted:
                GroupAdmins.objects.create(group_belong_to=self, buddy_profile_admin=admin)


class BuddyExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuddyExpense

    title = fake.sentence()
    buddy_group = factory.SubFactory('tests.factories_models_tests.BuddyGroupFactory')
    description = fake.text()
    total_amount = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
    currency = BuddyExpense.Currency.EUR

    @factory.post_generation
    def participants_of_expense_payment(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for participant in extracted:
                ParticipantsOfExpensePayment.objects.create(
                    expense=self,
                    participant_id=participant,
                    percentage_to_pay=fake.random_int(min=1, max=100),
                    amount_to_pay=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                    payment_balance=fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                )

    @factory.post_generation
    def payments_made_it_by_payers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for payer in extracted:
                PaymentsMadeItByPayers.objects.create(
                    what_expense_belong_to=self,
                    who_do_simple_payment=payer,
                    amount_payment=fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                )

    @factory.post_generation
    def settlement_by_participants(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for settler in extracted:
                SettlementByParticipants.objects.create(
                    what_expense_belong=self,
                    who_settle_simple_payment_up=settler,
                    amount_payment=fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                )
class SettlementByParticipantsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SettlementByParticipants

    who_settle_simple_payment_up = factory.SubFactory(BuddyProfileFactory)
    what_expense_belong = factory.SubFactory(BuddyExpenseFactory)
    amount_payment = fake.pydecimal(left_digits=3, right_digits=2, positive=True)