from groq import Groq

from django.conf import settings

from destinations.models import Destination


class TravelAssistant:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def build_trip_context(self, trip):

        destinations = Destination.objects.filter(
            trip=trip
        ).order_by("order")

        destination_text = ""

        for destination in destinations:

            destination_text += f"""
Destination {destination.order}
City: {destination.city}
State: {destination.state}
Country: {destination.country}
Type: {destination.place_type}
Estimated Cost: ₹{destination.estimated_cost}
Notes: {destination.notes}
"""

        context = f"""
Trip Name:
{trip.trip_name}

Start Date:
{trip.start_date}

End Date:
{trip.end_date}

Budget:
₹{trip.budget}

Travelers:
{trip.travelers}

Transport:
{trip.transport}

Destinations:

{destination_text}
"""

        return context

    def ask(self, trip, user_question):

        trip_context = self.build_trip_context(trip)

        system_prompt = f"""
You are an expert AI Travel Planner.

Use ONLY the trip information below.

{trip_context}

Your job is to help the traveler.

You can:

- Suggest better itineraries.
- Recommend nearby attractions.
- Recommend restaurants.
- Recommend hotels.
- Reduce trip budget.
- Improve route planning.
- Suggest packing list.
- Suggest best visiting time.
- Give travel tips.
- Recommend hidden gems.

Always answer clearly using bullet points whenever possible.
"""

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_question,
                },
            ],

            temperature=0.5,

            max_tokens=1200,
        )

        return response.choices[0].message.content