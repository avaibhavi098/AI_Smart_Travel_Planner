from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from trips.models import Trip

from .models import ChatMessage
from .services import TravelAssistant


@login_required
def chat_page(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )

    messages = ChatMessage.objects.filter(
        trip=trip
    )

    return render(
        request,
        "assistant_ai/chat.html",
        {
            "trip": trip,
            "messages": messages,
        },
    )


@login_required
@require_POST
def send_message(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )

    user_message = request.POST.get(
        "message",
        ""
    ).strip()

    if not user_message:

        return JsonResponse(
            {
                "success": False,
                "error": "Message cannot be empty."
            },
            status=400,
        )

    ChatMessage.objects.create(
        trip=trip,
        role="user",
        message=user_message,
    )

    assistant = TravelAssistant()

    ai_reply = assistant.ask(
        trip,
        user_message,
    )

    ChatMessage.objects.create(
        trip=trip,
        role="assistant",
        message=ai_reply,
    )

    return JsonResponse(
        {
            "success": True,
            "reply": ai_reply,
        }
    )


@login_required
def chat_history(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )

    messages = ChatMessage.objects.filter(
        trip=trip
    ).values(
        "role",
        "message",
        "created_at",
    )

    return JsonResponse(
        {
            "messages": list(messages),
        }
    )