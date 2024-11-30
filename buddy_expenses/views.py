from rest_framework import generics, status
from rest_framework.generics import ListAPIView, CreateAPIView
from django.db.models import Q

from buddy_expenses.models import BuddyExpense, SettlementByParticipants
from buddy_expenses.serializers import BuddyExpenseSerializer, BuddyExpenseCreateSerializer, \
    SettleParticipantExpenseUpSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from buddy_profiles.models import BuddyProfile


class BuddyExpenseListCreateView(generics.ListCreateAPIView):
    queryset = BuddyExpense.objects.all()
    serializer_class = BuddyExpenseSerializer
    permission_classes = [IsAuthenticated]


    @extend_schema(
        request=BuddyExpenseSerializer,
        responses={201: BuddyExpenseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BuddyExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuddyExpense.objects.all()
    serializer_class = BuddyExpenseSerializer
    permission_classes = [IsAuthenticated]


    @extend_schema(
        request=BuddyExpenseSerializer,
        responses={200: BuddyExpenseSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        request=BuddyExpenseSerializer,
        responses={200: BuddyExpenseSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.deleted_date = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuddyExpensesOfOneProfileListAPIView(ListAPIView):
    serializer_class = BuddyExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user_authenticated = BuddyProfile.objects.get(user=self.request.user)
        expenses = BuddyExpense.objects.filter(Q(participants_of_expense_payment=user_authenticated) )
        return expenses

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class BuddyExpensesOfOneGroupListAPIView(ListAPIView):
    serializer_class = BuddyExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        expenses = BuddyExpense.objects.filter(buddy_group_id=group_id)
        return expenses

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Instantiate the serializer
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)

        # Return the serialized data
        return Response(serializer.data)


class CreateExpenseOfUserAuthenticated(CreateAPIView):
    serializer_class = BuddyExpenseCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['admin'] = self.request.user
        return context

    @extend_schema(
        request=BuddyExpenseCreateSerializer,
        responses={201: BuddyExpenseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BuddySettleUpOfExpensesListAPIView(ListAPIView):
    serializer_class = SettleParticipantExpenseUpSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        settle_id = self.kwargs.get('pk')
        settles = SettlementByParticipants.objects.filter(what_expense_belong__id=settle_id)
        return settles

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Instantiate the serializer
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)

        # Return the serialized data
        return Response(serializer.data)