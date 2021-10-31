from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import csv
import speech_recognition as sr

with open('C:\\Users\\Vaishnavi Mall\\Downloads\\Jigyasa_questions.csv', 'r', encoding="utf8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    training_data_list = []
    for row in spamreader:
        training_data_list.append(','.join(row))


class LandingPageView(View):
    template_name = 'dev/landing_page.html'
    jigyasa = ChatBot("jigyasa")
    conversation = training_data_list

    trainer = ListTrainer(jigyasa)
    trainer.train(conversation)

    def get(self, request):
        if request.GET.get("action"):
            try:
                res = str(self.jigyasa.get_response(request.GET.get("user_input")))
            except Exception:
                res = "Sorry I don't know about it but will surely look into this."
            return JsonResponse({"res": res})
        return render(request, self.template_name)


class MicView(View):
    def get(self, request):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            text = str(r.recognize_google(audio))
            return JsonResponse({"res": text})
