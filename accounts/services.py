import random


class OTPService:


    @staticmethod
    def generate():

        return str(
            random.randint(
                100000,
                999999
            )
        )