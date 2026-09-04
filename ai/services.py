from groq import Groq
from django.conf import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


class AIItineraryService:


    @staticmethod
    def generate_itinerary(trip, destinations):


        destination_list = "\n".join(
            [
                f"{index}. {destination.city}"
                for index, destination in enumerate(
                    destinations,
                    start=1
                )
            ]
        )


        interests = ", ".join(
            trip.interests
        ) if trip.interests else "No specific interests"



        prompt = f"""

You are an expert AI travel planner.

Generate a complete ROUND TRIP itinerary in MARKDOWN format.



IMPORTANT TRAVEL RULES:

1. The traveller starts the journey from the source location.
2. Visit destinations exactly in the given order.
3. Do not rearrange destinations.
4. The trip MUST end by returning back to the original source location.
5. Do not stop the itinerary at the last destination.
6. Include the complete return journey.
7. Mention realistic transport details for every major travel movement.
8. Plan according to traveller preferences and budget.
9. Always provide estimated travel expenses.



Trip Name:

{trip.trip_name}



Starting Location:

{trip.source_city}, {trip.source_country}



Destination Order:

{destination_list}



Trip Details:

Budget:
₹{trip.budget}


Travelers:
{trip.travelers}


Transport Preference:
{trip.transport}


Travel Style:
{trip.travel_style}


Food Preference:
{trip.food_preference}


Budget Priority:
{trip.budget_priority}


Traveller Interests:
{interests}



Start Date:

{trip.start_date}



End Date:

{trip.end_date}




Generate:



# Trip Overview

Explain the complete round trip.

Mention:

- Starting location
- Destination sequence
- Return journey plan
- Overall estimated budget



## Day 1

Start from the source location.



For every day include:



### Activities

- Morning activities
- Afternoon activities
- Evening activities
- Places to visit
- Approximate timings



### Transportation Details

For every travel movement mention:

- Starting point
- Destination point
- Transport mode
- Route
- Distance
- Approximate duration
- Departure timing
- Arrival timing
- Estimated fare
- Booking method



### Daily Expense Breakdown

Include:

- Transport cost
- Food cost
- Entry ticket cost
- Accommodation cost if required
- Other expenses
- Total estimated daily cost



### Food Recommendations

Suggest food based on:

{trip.food_preference}



### Travel Tips

Include:

- Booking advice
- Best travel time
- Safety tips
- Local guidance





FINAL DAY RULE:

The final day must include:

- Last destination activities
- Starting return journey
- Return route to source location
- Transport mode
- Distance
- Travel duration
- Departure time
- Arrival time
- Estimated return fare



Finally include:



# Budget Summary

Include:

- Transportation total
- Accommodation total
- Food total
- Activities total
- Overall estimated trip cost



# Packing Checklist



# Important Travel Tips



Return ONLY markdown.

"""


        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            temperature=0.3,

            max_tokens=3000,

        )


        return response.choices[0].message.content