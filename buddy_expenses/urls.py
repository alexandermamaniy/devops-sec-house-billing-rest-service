from django.urls import path
from .views import BuddyExpensesOfOneProfileListAPIView, BuddyExpensesOfOneGroupListAPIView, CreateExpenseOfUserAuthenticated, BuddySettleUpOfExpensesListAPIView, BuddySettleUpParticipantPostView

urlpatterns = [
    path('buddy-expenses/me', BuddyExpensesOfOneProfileListAPIView.as_view(), name='buddy-expenses-profile'),
    path('buddy-expenses/group/<uuid:pk>', BuddyExpensesOfOneGroupListAPIView.as_view(), name='buddy-expenses-group'),
    path('buddy-expenses/settle-up/<uuid:pk>', BuddySettleUpOfExpensesListAPIView.as_view(), name='buddy-expenses-settle-up'),
    path('buddy-expenses/settle-up-participant', BuddySettleUpParticipantPostView.as_view(), name='buddy-expenses-settle-up-participant'),
    path('buddy-expenses/', CreateExpenseOfUserAuthenticated.as_view(), name='buddy-expenses-create'),
]
