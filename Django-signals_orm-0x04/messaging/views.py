from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return HttpResponse("Your account has been deleted successfully.")
    return HttpResponse("Send a POST request to delete your account.")

@method_decorator(cache_page(60), name='dispatch')
class ConversationMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        conv_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conv_id).select_related('sender', 'receiver')
