from flask import Flask, render_template, url_for, request, jsonify
import numpy as np
import pickle
import requests
import json
from bs4 import BeautifulSoup
app = Flask(__name__) 

loaded_model = pickle.load(open("model.sav", "rb"))

symptoms_dict = {
    "abdominal_pain": 39,
    "abnormal_menstruation": 101,
    "acidity": 8,
    "acute_liver_failure": 44,
    "altered_sensorium": 98,
    "anxiety": 16,
    "back_pain": 37,
    "belly_pain": 100,
    "blackheads": 123,
    "bladder_discomfort": 89,
    "blister": 129,
    "blood_in_sputum": 118,
    "bloody_stool": 61,
    "blurred_and_distorted_vision": 49,
    "breathlessness": 27,
    "brittle_nails": 72,
    "bruising": 66,
    "burning_micturition": 12,
    "chest_pain": 56,
    "chills": 5,
    "cold_hands_and_feets": 17,
    "coma": 113,
    "congestion": 55,
    "constipation": 38,
    "continuous_feel_of_urine": 91,
    "continuous_sneezing": 3,
    "cough": 24,
    "cramps": 65,
    "dark_urine": 33,
    "dehydration": 29,
    "depression": 95,
    "diarrhoea": 40,
    "dischromic _patches": 102,
    "distention_of_abdomen": 115,
    "dizziness": 64,
    "drying_and_tingling_lips": 76,
    "enlarged_thyroid": 71,
    "excessive_hunger": 74,
    "extra_marital_contacts": 75,
    "family_history": 106,
    "fast_heart_rate": 58,
    "fatigue": 14,
    "fluid_overload": 45,
    "fluid_overload.1": 117,
    "foul_smell_of urine": 90,
    "headache": 31,
    "high_fever": 25,
    "hip_joint_pain": 79,
    "history_of_alcohol_consumption": 116,
    "increased_appetite": 104,
    "indigestion": 30,
    "inflammatory_nails": 128,
    "internal_itching": 93,
    "irregular_sugar_level": 23,
    "irritability": 96,
    "irritation_in_anus": 62,
    "itching": 0,
    "joint_pain": 6,
    "knee_pain": 78,
    "lack_of_concentration": 109,
    "lethargy": 21,
    "loss_of_appetite": 35,
    "loss_of_balance": 85,
    "loss_of_smell": 88,
    "malaise": 48,
    "mild_fever": 41,
    "mood_swings": 18,
    "movement_stiffness": 83,
    "mucoid_sputum": 107,
    "muscle_pain": 97,
    "muscle_wasting": 10,
    "muscle_weakness": 80,
    "nausea": 34,
    "neck_pain": 63,
    "nodal_skin_eruptions": 2,
    "obesity": 67,
    "pain_behind_the_eyes": 36,
    "pain_during_bowel_movements": 59,
    "pain_in_anal_region": 60,
    "painful_walking": 121,
    "palpitations": 120,
    "passage_of_gases": 92,
    "patches_in_throat": 22,
    "phlegm": 50,
    "polyuria": 105,
    "prominent_veins_on_calf": 119,
    "puffy_face_and_eyes": 70,
    "pus_filled_pimples": 122,
    "receiving_blood_transfusion": 111,
    "receiving_unsterile_injections": 112,
    "red_sore_around_nose": 130,
    "red_spots_over_body": 99,
    "redness_of_eyes": 52,
    "restlessness": 20,
    "runny_nose": 54,
    "rusty_sputum": 108,
    "scurring": 124,
    "shivering": 4,
    "silver_like_dusting": 126,
    "sinus_pressure": 53,
    "skin_peeling": 125,
    "skin_rash": 1,
    "slurred_speech": 77,
    "small_dents_in_nails": 127,
    "spinning_movements": 84,
    "spotting_ urination": 13,
    "stiff_neck": 81,
    "stomach_bleeding": 114,
    "stomach_pain": 7,
    "sunken_eyes": 26,
    "sweating": 28,
    "swelled_lymph_nodes": 47,
    "swelling_joints": 82,
    "swelling_of_stomach": 46,
    "swollen_blood_vessels": 69,
    "swollen_extremeties": 73,
    "swollen_legs": 68,
    "throat_irritation": 51,
    "toxic_look_(typhos)": 94,
    "ulcers_on_tongue": 9,
    "unsteadiness": 86,
    "visual_disturbances": 110,
    "vomiting": 11,
    "watering_from_eyes": 103,
    "weakness_in_limbs": 57,
    "weakness_of_one_body_side": 87,
    "weight_gain": 15,
    "weight_loss": 19,
    "yellow_crust_ooze": 131,
    "yellow_urine": 42,
    "yellowing_of_eyes": 43,
    "yellowish_skin": 32,
}


@app.route("/predict/<sym>", methods = ["GET"])
def home(sym):
    input_vector = np.zeros(len(symptoms_dict))
    symp = []
    symptoms = sym.split(",")

    for symptom in symptoms:
        symp.append(symptoms_dict[symptom])

    input_vector[symp] = 1

    return jsonify({"data": loaded_model.predict([input_vector])[0]})


@app.route("/disease/<d>", methods = ["GET"])
def root(d):
    url = "https://en.wikipedia.org/wiki/" + d
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pAll = soup.find_all("p")
    if(pAll[0].get_text != '\n'):
        return jsonify({"para": pAll[0].get_text()})
    else:
        return jsonify({"para": pAll[1].get_text()})


@app.route("/<num>", methods = ['GET'])
def index(num):
    names = []
    res = {}
    exp = []
    q = []
    # a = request._json
    # x = json.loads(a)
    url = "https://www.practo.com/" + str(num) +"/doctors"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    exp_temp = soup.find_all("h3", attrs = {'data-qa-id': 'doctor_experience'})
    names_temp = soup.find_all("h2", attrs = {'data-qa-id': 'doctor_name'})
    q_temp = soup.find_all("div", attrs = {"data-qa-id": "doctor_qualification"})
    for i in range(len(names_temp)):
        res[str(i)] = {"name": names_temp[i].get_text(), "exp": exp_temp[i].get_text(), "q": q_temp[i].get_text()}
    for x in names_temp:
        names.append(x.get_text())
    # for x in exp_temp:
    #     exp.append(x.get_text())
    # for x in q_temp:
    #     q.append(x.get_text())
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)