import requests
from django.conf import settings


class GeoapifyService:

    BASE_URL = "https://api.geoapify.com/v1/geocode/search"


    @staticmethod
    def search_places(query, limit=5):

        if not query:
            return []


        try:

            response = requests.get(

                GeoapifyService.BASE_URL,

                params={

                    "text": query,

                    "limit": limit,

                    "apiKey": settings.GEOAPIFY_API_KEY,

                },

                timeout=10,

            )


            print("Status:", response.status_code)

            print(
                "Response:",
                response.text[:300]
            )


            response.raise_for_status()


            data = response.json()


        except Exception as e:

            print(
                "Geoapify Error:",
                e
            )

            return []


        places = []


        for item in data.get("features", []):

            properties = item.get(
                "properties",
                {}
            )


            places.append(

                {

                    "display_name":
                        properties.get(
                            "formatted",
                            ""
                        ),


                    "city":
                        properties.get(
                            "city",
                            ""
                        ),


                    "state":
                        properties.get(
                            "state",
                            ""
                        ),


                    "country":
                        properties.get(
                            "country",
                            ""
                        ),


                    "latitude":
                        properties.get(
                            "lat"
                        ),


                    "longitude":
                        properties.get(
                            "lon"
                        ),

                }

            )


        return places



    @staticmethod
    def get_location(query):

        places = GeoapifyService.search_places(

            query,

            limit=1

        )


        return places[0] if places else None