<<<<<<< HEAD
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
=======
from rest_framework import viewsets, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message, Book
from .serializers import ConversationSerializer, MessageSerializer, BookSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
>>>>>>> 9495c56 (Update messaging_app with filters and views)

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']  # Example, adapt as needed

    def create(self, request, *args, **kwargs):
        # Add custom logic here if needed
        return super().create(request, *args, **kwargs)

# Message ViewSet with custom queryset and filtering
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
<<<<<<< HEAD
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']

    def create(self, request, *args, **kwargs):
        # Add custom logic here if needed
        return super().create(request, *args, **kwargs)
=======
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        # Only return messages in conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

# Book API (List and Create)
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

>>>>>>> 9495c56 (Update messaging_app with filters and views)
