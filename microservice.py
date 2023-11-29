from pydub import AudioSegment, utils
import json
import time


def mix_audio(data):
    tracks = [AudioSegment.from_file(track, format="wav") for track in data['tracks']]
    
    if len(data['tracks']) < 2:
        print("Error: Must overlay 2 or more tracks.")
        clear(data)
        return
    
    output = tracks[0]                    # overlay starting at first track then overlays the rest of the array
    for track in tracks[1:]:
        output = output.overlay(track)

    output.export(data['output'], format="wav")
    print(f"\nMixed tracks to {data['output']}...\n")
    clear(data)
    
def adjust_volume(data):
    tracks = [AudioSegment.from_file(track, format="wav") for track in data['tracks']]
    
    if len(tracks) == 0:
        print("Error: Must have 1 track to adjust audio.")
        clear(data)
        return
    
    volume_db = utils.ratio_to_db(data['volume_scale'])
    adjusted_tracks = [track.apply_gain(volume_db) for track in tracks]     #adjusts volume with a min range of 0.0 
    
    output = sum(adjusted_tracks)
    output.export(data['output'], format="wav")
    print(f"\nAdjusted volume by {data['volume_scale']} and saved to {data['output']}...\n")
    clear(data)
    

def clear(data):
    with open('remix-choice.json', 'w') as json_file:
        data['command'] = ""
        data['tracks'] = []
        data['output'] = ""
        data['volume_scale'] = 1
        json.dump(data, json_file, indent=4)

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

try:
    with open('remix-choice.json', 'r') as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    print("File not found... Creating file...")
    time.sleep(2)
    data = {
        "command": "",
        "tracks": [],
        "output": "",
        "volume_scale": 1,
    }
    save_to_json(data)

print("Waiting for request...")

while True:
    current_data = get_json_data()
    if current_data.get('command', '') != "":
        break
    time.sleep(1)
    
match current_data['command']:
    case "mix":
        mix_audio(current_data)
    case "volume":
        adjust_volume(current_data)
    case _:
        print("Invalid command.\n")
        clear(current_data)