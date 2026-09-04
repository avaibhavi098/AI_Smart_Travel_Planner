import requests


class OSRMService:

    BASE_URL = "https://router.project-osrm.org/trip/v1/driving/"


    @staticmethod
    def optimize_route(destinations):

        if len(destinations) < 2:
            return None


        valid_destinations = [
            destination
            for destination in destinations
            if destination.latitude is not None
            and destination.longitude is not None
        ]


        if len(valid_destinations) < 2:
            return None



        coordinates = ";".join(

            f"{destination.longitude},{destination.latitude}"

            for destination in valid_destinations

        )



        url = (

            f"{OSRMService.BASE_URL}"

            f"{coordinates}"

            "?source=first"

            "&destination=last"

            "&roundtrip=false"

            "&overview=full"

            "&geometries=geojson"

            "&steps=true"

        )



        try:

            response = requests.get(
                url,
                timeout=20,
            )


            response.raise_for_status()


            data = response.json()



            if data.get("code") != "Ok":

                return None



            trips = data.get(
                "trips",
                []
            )


            waypoints = data.get(
                "waypoints",
                []
            )



            if not trips or not waypoints:

                return None



            return {

                "trips": trips,

                "waypoints": waypoints,

            }



        except requests.RequestException as e:

            print(
                "OSRM Request Error:",
                e
            )

            return None



        except Exception as e:

            print(
                "OSRM Error:",
                e
            )

            return None