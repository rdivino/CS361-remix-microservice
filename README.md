# CS361-remix-microservice

Install pydub and ffmpeg for remixing audio
```
pip install pydub
pip install ffmpeg
```
To make a request you must write into remix-choice.json the 'choice' ("mix", "increase", "decrease", "reverse") and audio 'track1' and 'track2'("first", "last") to then send to the remix-microservice to manipulate the audio.   
  
Example requesting data:  
```
import json

# opening json file
with open('remix-choice.json', 'r+') as file:
        data = json.load(file)


# adds {"choice": "mix"} into json file
data['choice'] = "mix"
mix_audio(data)


# adds both tracks into each other mixing them together
def mix_audio(data):
    print("1. track 1 + track 2")
    print("2. track 2 + track 1")
    track = input("How would you like the audio mixed? ")
    
    match track:
        case "1": 
            data['track1'] = "first"
            data['track2'] = "last"
            print("\nmixed tracks to output.wav...\n")  
            save_to_json(data)
        case "2":
            data['track1'] = "last"
            data['track2'] = "first"
            print("\nmixed tracks to output.wav...\n") 
            save_to_json(data)
        case _:
            print("Invalid choice. Cleared data\n")
            clear(data)

#saves data into remix-choice.json
def save_to_json(remix_data):
    with open('remix-choice.json', 'w') as json_file:
        json.dump(remix_data, json_file, indent=4)

```  
  
To receive data, the remix-microservice will read the json file and will loop until an object("mix", "increase", "decrease", "reverse") is added into 'choice' in remix-choice.json file. 
When the choice is added it will then run the choice's function and will check the json on what tracks(track1, track2) will be mixed or manipulated ("first", "last") into output.wav.  

Example receiving data:   
```
from pydub import AudioSegment
import json
import time

def clear(data):
    with open('remix-choice.json', 'w') as json_file:
        data['choice'] = ""
        data['track1'] = ""
        data['track2'] = "" 
        json.dump(data, json_file, indent=4)

audio1 = AudioSegment.from_file("StarWars3.wav", format="wav")
audio2 = AudioSegment.from_file("CantinaBand3.wav", format="wav")

with open('remix-choice.json', 'r+') as file:
        data = json.load(file)

if data['choice'] == "mix":
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
else:
  print("Invalid choice.\n")
  clear(data)

    
```

![umldiagram_remix](https://github.com/rdivino/CS361-remix-microservice/assets/61130026/c73a7f4a-0aaf-4a16-83af-af0a04371d2f)

