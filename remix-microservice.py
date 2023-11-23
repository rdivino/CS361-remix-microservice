#program reads choice from json file then outputs track
from pydub import AudioSegment
import json
import time

# Load an audio file (replace wav files with the path to your audio file)
audio1 = AudioSegment.from_file("StarWars3.wav", format="wav")
audio2 = AudioSegment.from_file("CantinaBand3.wav", format="wav")

#mixes tracks together
def mix_audio(data):   
    if data['track1'] == "first":
        output = audio1 + audio2
        output.export("output.wav", format = "wav")
        print("\nmixed track 1 to track 2 to output.wav...\n")  
        clear(data)
    elif data['track1'] == "last":
        output = audio2 + audio1
        output.export("output.wav", format = "wav")
        print("\nmixed track 2 to track 1 to output.wav...\n") 
        clear(data)
    else: 
        print("Error.\n")
        clear(data)
        

 #increase audio volume by 10 dB   
def boost_volume(data):
    if data['track1'] == "first":
        volume_adjusted_audio = audio1 + 10
        volume_adjusted_audio.export("output.wav", format="wav") 
        print("\nincreased track 1 audio by 10 dB to output.wav...\n")
        clear(data)   
    elif data['track2'] == "last":
        volume_adjusted_audio = audio2 + 10
        print("\nincreased track 2 audio by 10 dB to output.wav...\n") 
        clear(data)
        volume_adjusted_audio.export("output.wav", format="wav")
    else: 
        print("Error.\n")
        clear(data)

 #decrease audio volume by 10 dB    
def reduce_volume(data):
    if data['track1'] == "first":
        volume_adjusted_audio = audio1 - 10
        print("\ndecreased track 1 audio by 10 dB to output.wav...\n") 
        volume_adjusted_audio.export("output.wav", format="wav")  
        clear(data)
    elif data['track2'] == "last":
        volume_adjusted_audio = audio2 - 10
        print("\ndecrease track 2 audio by 10 dB to output.wav...\n") 
        volume_adjusted_audio.export("output.wav", format="wav")
        clear(data)
    else: 
        print("Error.\n")
        clear(data)
    
 #reverse playback track audio   
def reverse_audio(data):
    if data['track1'] == "first":
        reversed_audio = audio1.reverse()
        print("\nreversed track1 to output.wav...\n")  
        reversed_audio.export("output.wav", format="wav")
        clear(data)
    elif data['track2'] == "last":
        reversed_audio = audio2.reverse()
        print("\nreversed track2 to output.wav...\n") 
        reversed_audio.export("output.wav", format="wav")
        clear(data)
    else: 
        print("Error.\n")
        clear(data)

#clears json data for next request
def clear(data):
    with open('remix-choice.json', 'w') as json_file:
        data['choice'] = ""
        data['track1'] = ""
        data['track2'] = "" 
        json.dump(data, json_file, indent=4)  
        
#used to loop through json until data is found
def get_json_data(): 
    try:
        with open('remix-choice.json', 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return {}
    
    
def save_to_json(remix_data):
    with open('remix-choice.json', 'w') as json_file:
        json.dump(remix_data, json_file, indent=4)
    
print("Starting Audio Remix microservice...")
time.sleep(1)

#creates json file if not found
try:
    with open('remix-choice.json', 'r+') as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    print("File not found... Creating file...")
    
    time.sleep(2)
    
    data = {
        "choice": "",
        "track1": "",
        "track2": "",
    }
    save_to_json(data)


print("waiting for request...")

while True:  #loops through json until data is found
    current_data = get_json_data()
    if current_data.get('choice', '') != "":
        break
    
    time.sleep(1)
    
match current_data['choice']:
    case "mix": 
        mix_audio(current_data)
    case "increase":
        boost_volume(current_data)
    case "decrease":
        reduce_volume(current_data)
    case "reverse":
        reverse_audio(current_data)
    case _:
        print("Invalid choice.\n")
        
    