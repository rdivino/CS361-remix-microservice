#program inputs choice into json file.
import json
import time



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
    
def boost_volume(data):
    print("1. track 1")
    print("2. track 2")
    track = input("What track would you like to increase volume? ")
    
    match track:
        case "1": 
            data['track1'] = "first"
            data['track2'] = ""
            print("\nincreased track 1 audio by 10 dB...\n")
            save_to_json(data)
        case "2":
            data['track1'] = ""
            data['track2'] = "last"
            print("\nincreased track 2 audio by 10 dB...\n") 
            save_to_json(data)
        case _:
            print("Invalid choice. Cleared data\n")
            clear(data)
    
def reduce_volume(data):
    print("1. track 1")
    print("2. track 2")
    track = input("What track would you like to decrease volume? ")
    
    match track:
        case "1": 
            data['track1'] = "first"
            data['track2'] = ""
            print("\ndecreased track 1 audio by 10 dB...\n") 
            save_to_json(data)
        case "2":
            data['track1'] = ""
            data['track2'] = "last"
            print("\ndecreased track 2 audio by 10 dB...\n")
            save_to_json(data)  
        case _:
            print("Invalid choice. Cleared data\n")
            clear(data)
    
def reverse_audio(data):
    print("1. track 1")
    print("2. track 2")
    track = input("What track would you like to reverse? ")

    match track:
        case "1": 
            data['track1'] = "first"
            data['track2'] = ""
            print("\nreversed track1 to output.wav...\n") 
            save_to_json(data)
        case "2":
            data['track1'] = ""
            data['track2'] = "last"
            print("\nreversed track2 to output.wav...\n") 
            save_to_json(data) 
        case _:
            print("Invalid choice. Cleared data\n")
            clear(data)

def clear(data):
    data['choice'] = ""
    data['track1'] = ""
    data['track2'] = "" 
    save_to_json(data)

def save_to_json(remix_data):
    with open('remix-choice.json', 'w') as json_file:
        json.dump(remix_data, json_file, indent=4)

print("\nRunning audio remix microservice...")
print("Choice 1: Mix audio files")
print("Choice 2: Increase volume")
print("Choice 3: Decrease volume")
print("Choice 4: Reverse track")
choice = input("Input a option (1-4): ")

#creates json file if not found
try:
    with open('remix-choice.json', 'r+') as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    print("\nFile not found... Creating file...\n")
    
    time.sleep(2)
    
    data = {
        "choice": "",
        "track1": "",
        "track2": "",
    }
    save_to_json(data) 
    
match choice:
    case "1":
        data['choice'] = "mix"
        mix_audio(data)
    case "2":
        data['choice'] = "increase"
        boost_volume(data)
    case "3":
        data['choice'] = "decrease"
        reduce_volume(data)
    case "4":
        data['choice'] = "reverse"
        reverse_audio(data) 
    case _:
        print("Invalid choice. Cleared data\n")
        clear(data)
        