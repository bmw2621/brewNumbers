from flask import Flask, request
from flask_restful import Resource, Api
from formulas import *

app = Flask(__name__)
api = Api(app)

class CorrectedTemps(Resource):


    def get(self, original_gravity, original_temp, final_gravity, final_temp):
        corrected_original_gravity = round(corrected_sg(original_gravity, original_temp), 3)
        corrected_final_gravity = round(corrected_sg(final_gravity, final_temp), 3)
        response = {
            "provided" : {
                "original_gravity": original_gravity,
                "original_temp": original_temp,
                "final_gravity": final_gravity,
                "final_temp": final_temp
            },
            "corrected_original_gravity": corrected_original_gravity,
            "corrected_final_gravity": corrected_final_gravity,
            "alcohol_content": round(alcohol_content(corrected_original_gravity, corrected_final_gravity), 3),
            "attenuation": round(real_attenuation(original_gravity, final_gravity), 3),
            "calories": round(calories(original_gravity, final_gravity), 3)
        }
        return response


class GravitiesOnly(Resource):


    def get(self, original_gravity, final_gravity):
        response = {
            "provided" : {
                "original_gravity": original_gravity,
                "final_gravity": final_gravity,
            },
            "alcohol_content": round(alcohol_content(original_gravity, final_gravity), 3),
            "attenuation": round(real_attenuation(original_gravity, final_gravity), 3),
            "calories": round(calories(original_gravity, final_gravity), 3)
        }
        return response


class HowMuchSugar(Resource):


    def get(self, temp_f, desired_co2, volume_beer_gallons):
        response = {
            "provided": {
                "temp_in_f": temp_f,
                "desired_co2": desired_co2,
                "volume_beer_gallons": volume_beer_gallons
            },
            "req_gramms_priming_sugar": how_much_sugar(temp_f, desired_co2, volume_beer_gallons)
        }
        return response


class HowMuchCO2(Resource):


    def get(self, temp_f, priming_sugar_grams, volume_beer_gallons):
        response = {
            "provided": {
                "temp_in_f": temp_f,
                "priming_sugar_grams": priming_sugar_grams,
                "volume_beer_gallons": volume_beer_gallons
            },
            "req_gramms_priming_sugar": round(carbon_dioxide(temp_f, priming_sugar_grams, volume_beer_gallons), 2)
        }
        return response


api.add_resource(GravitiesOnly, '/<float:original_gravity>/'
                                '<float:final_gravity>')
api.add_resource(CorrectedTemps, '/tempcorrected/<float:original_gravity>/'
                                 '<int:original_temp>/'
                                 '<float:final_gravity>/'
                                 '<int:final_temp>')
api.add_resource(HowMuchSugar, '/carbonation/howmuchsugar/<int:temp_f>/'
                               '<float:desired_co2>/'
                               '<float:volume_beer_gallons>')
api.add_resource(HowMuchCO2, '/carbonation/howmuchco2/<int:temp_f>/'
                             '<float:priming_sugar_grams>/'
                             '<float:volume_beer_gallons>')


if __name__ == "__main__":
    app.run(port=8080, debug=False)