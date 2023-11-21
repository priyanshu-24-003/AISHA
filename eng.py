import os
import openai
import ApiKey
import speech_recognition as sr
import platform
from gtts import gTTS
from playsound import playsound
import multiprocessing


class Chat:

	def __init__(self, user):
		self.conversation = ''
		self.username = user
		self.bot = "AISHA"
		pass

	def Talk(self,):
		#Coroutine to give gpt-3 based output 
		openai.api_key = ApiKey.api_key
		model_engine = "text-davinci-003"

		response_str = ""
		while True:

			user_input = yield response_str
			prompt = self.username + ": " + user_input + "\n" + self.bot+ ": "

			self.conversation += prompt

			response = openai.Completion.create(engine='text-davinci-003', prompt=self.conversation, max_tokens=100)
			response_str = response["choices"][0]["text"].replace("\n", "")
			response_str = response_str.split(self.username + ": ", 1)[0].split(self.bot + ": ", 1)[0]

			self.conversation += response_str + "\n"

	def listen(self,):
		r = sr.Recognizer()

		with sr.Microphone() as source:
		
			r.adjust_for_ambient_noise(source)
			print("Please say something")
			audio = r.listen(source, phrase_time_limit=10)
			print("Recognizing Now .... ")

			try:
			    aa = r.recognize_google(audio)
			    return aa 
			except Exception as e:
			    return input("Now You Have To Write: ")

			with open("recorded.wav", "wb") as f:
			    f.write(audio.get_wav_data())


	def say(self, query):
		p = platform.system()
		if p == 'Linux':
			# sudo apt-get install festival festvox-us-slt-hts
			os.system(f"""echo "{query}" | festival --tts""")
		elif p == 'Windows':
			# os.system(f"""mshta vbscript:Execute("CreateObject(""SAPI.SpVoice"").Speak(""{query}"")(window.close)")""")
			tts = gTTS(text=query, lang='en')
			tts.save('file1.mp3')
			p = multiprocessing.Process(target=playsound, args=("file1.mp3",))
			p.start()
			input("next")
			p.terminate()
			pass

			
if __name__ == '__main__':
	
	c = Chat('Priyanshu')
	r = c.Talk() 
	next(r)
	
	while True:
		io = c.listen()
		if io == 'the end':
			break
		print(f'{c.username} : {io}')
		try:
			response = str(r.send(io))
		except Exception as e:
			response = 'Your Basic Plan Has Been Exausted'
		print(response)
		c.say(response)

	print()
	print('entire conversation'.upper())
	print(c.conversation)
