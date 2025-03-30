import os
import platform
import json
import shutil
import base64
import requests
import urllib.parse
import subprocess
import zipfile
import tempfile
import threading
import sys
import time
import inquirer
import socket
from PIL import Image

# variables
MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
    " ": "/",
    "\n": ".-.-",
}


# file operations and more
def write(file_name, mode, content):
    try:
        full_path = os.path.join(os.getcwd(), file_name)  
        with open(full_path, mode) as file:
            if isinstance(content, dict) or isinstance(content, list):
                content = json.dumps(content, indent=4)
            file.write(content)
        return True
    except IOError as e:
        print(f"\033[31m[ERROR] Failed to write to file: {e}\033[0m")
        return False

def read(file_name):
    try:
        full_path = os.path.join(os.getcwd(), file_name)  
        with open(full_path, "r") as file:
            return file.read()
    except IOError as e:
        print(f"\033[31m[ERROR] Failed to read file: {e}\033[0m")
        return ""

def append(file_name, content):
    return write(file_name, "a", content)

def fileExists(file_name):
    full_path = os.path.join(os.getcwd(), file_name)  
    return os.path.exists(full_path)

def fileSize(file_name):
    try:
        full_path = os.path.join(os.getcwd(), file_name)  
        return os.path.getsize(full_path)
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to get file size: {e}\033[0m")
        return -1

def deleteFile(file_name):
    try:
        full_path = os.path.join(os.getcwd(), file_name)  
        os.remove(full_path)
        return True
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to delete file: {e}\033[0m")
        return False

def rename(old_name, new_name):
    try:
        old_full_path = os.path.join(os.getcwd(), old_name) 
        new_full_path = os.path.join(os.getcwd(), new_name) 
        os.rename(old_full_path, new_full_path)
        return True
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to rename file: {e}\033[0m")
        return False

def fileCopy(src, dest):
    try:
        src_full_path = os.path.join(os.getcwd(), src) 
        dest_full_path = os.path.join(os.getcwd(), dest) 
        shutil.copy(src_full_path, dest_full_path)
        return True
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to copy file: {e}\033[0m")
        return False

def zip_files(file_list, zip_file_name):
    try:
        zip_full_path = os.path.join(os.getcwd(), zip_file_name) 
        with zipfile.ZipFile(zip_full_path, 'w') as zipf:
            for file in file_list:
                file_full_path = os.path.join(os.getcwd(), file) 
                zipf.write(file_full_path, os.path.basename(file))
        return True
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to zip files: {e}\033[0m")
        return False

def unzip_files(zip_file_name, extract_to):
    try:
        zip_full_path = os.path.join(os.getcwd(), zip_file_name) 
        extract_full_path = os.path.join(os.getcwd(), extract_to) 
        with zipfile.ZipFile(zip_full_path, 'r') as zipf:
            zipf.extractall(extract_full_path)
        return True
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to unzip files: {e}\033[0m")
        return False


# python commands
def printPy(message):
    print(message)


def inputPy(prompt):
    return input(prompt)


def execPy(code):
    try:
        if os.path.exists(code):
            with open(code, "r") as file:
                code = file.read()

        exec(code)
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to execute code: {e}\033[0m")


# system
def get_system_info():
    return {
        "OS": platform.system(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Python Version": platform.python_version(),
    }


def command(cmd):
    try:
        os.system(cmd)
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to execute command: {e}\033[0m")

def playAudio(file_path: str) -> None:
    try:
        if file_path.startswith("http://") or file_path.startswith("https://"):
            response = requests.get(file_path)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(response.content)
                temp_file_name = temp_audio.name

            subprocess.run(["ffplay", "-nodisp", "-autoexit", temp_file_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.unlink(temp_file_name)
        else:
            subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to play audio: {e}\033[0m")


def getIp():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        public_ip = requests.get('https://api64.ipify.org?format=json').json()["ip"]
        return {"Local IP": local_ip, "Public IP": public_ip}
    except Exception as e:
        return {"Error": f"Failed to get IP: {e}"}


# string functions
def upper(text):
    return text.upper()


def lower(text):
    return text.lower()


def reverse(text):
    return text[::-1]


# JSON stuff
def prettyPrint(data):
    try:
        if isinstance(data, dict):
            data = json.dumps(data)
        parsed_json = json.loads(data)
        return json.dumps(parsed_json, indent=4)
    except json.JSONDecodeError as e:
        print(f"\033[31m[ERROR] Failed to parse JSON: {e}\033[0m")
        return ""


def jsonWrite(file_name, data):
    try:
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to write JSON to file: {e}\033[0m")
        return False


def jsonRead(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to read JSON from file: {e}\033[0m")
        return {}





# dictionary stuff
def dictionaryCreate(directory):
    try:
        full_path = os.path.join(os.getcwd(), directory) 
        os.makedirs(full_path, exist_ok=True)
        return True
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to create directory: {e}\033[0m")
        return False
def list_directory(directory):
    try:
        full_path = os.path.join(os.getcwd(), directory)  
        return os.listdir(full_path)
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to list directory: {e}\033[0m")
        return []
def directoryExists(directory):
    full_path = os.path.join(os.getcwd(), directory) 
    return os.path.isdir(full_path)

# decode and encode random stuff
def morseEncode(text):
    return " ".join(MORSE_CODE_DICT.get(c.upper(), "") for c in text)


def morseDecode(morse_code):
    reverse_morse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
    return "".join(reverse_morse_dict.get(code, "") for code in morse_code.split(" "))


def base64Encode(text):
    try:
        encoded_bytes = base64.b64encode(text.encode("utf-8"))
        return encoded_bytes.decode("utf-8")
    except Exception as e:
        print(f"\033[31m[ERROR] Base64 encoding failed: {e}\033[0m")
        return ""


def base64Decode(encoded_text):
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode("utf-8")
    except Exception as e:
        print(f"\033[31m[ERROR] Base64 decoding failed: {e}\033[0m")
        return ""


def binaryEncode(text):
    return " ".join(format(ord(c), "08b") for c in text)


def binaryDecode(binary_text):
    binary_values = binary_text.split(" ")
    return "".join(chr(int(bv, 2)) for bv in binary_values)

# https stuff
def httpGet(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"\033[31m[ERROR] GET request failed with status code {response.status_code}\033[0m")
            return None
    except requests.RequestException as e:
        print(f"\033[31m[ERROR] HTTP GET request failed: {e}\033[0m")
        return None

def httpPost(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"\033[31m[ERROR] POST request failed with status code {response.status_code}\033[0m")
            return None
    except requests.RequestException as e:
        print(f"\033[31m[ERROR] HTTP POST request failed: {e}\033[0m")
        return None

def urlEncode(text):
    return urllib.parse.quote(text)

def urlDecode(encoded_text):
    return urllib.parse.unquote(encoded_text)

def webDownload(url, destination):
    try:
        full_dest_path = os.path.join(os.getcwd(), destination) 
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        downloaded = 0
        animation_chars = ['\\', '|', '/', '-']
        animation_index = 0

        with open(full_dest_path, 'wb') as file:
            for data in response.iter_content(block_size):
                downloaded += len(data)
                file.write(data)
                percentage = (downloaded / total_size) * 100 if total_size else 0
                print(f"\rDownloading: {percentage:.2f}% {animation_chars[animation_index % len(animation_chars)]}", end="")
                animation_index += 1
        print("\nDownload complete!")
        return True
    except Exception as e:
        print(f"\n\033[31m[ERROR] Download failed: {e}\033[0m")
        return False

def ferdinhaUpload(file_path=None):
    url = "https://feridinha.com/upload"

    def choose_file():
        media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mp3', '.wav', '.ogg', '.flv', '.mkv', 'webp', '.avi', '.mov', '.wmv']
        file_choices = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f)) and any(f.lower().endswith(ext) for ext in media_extensions)]
        if not file_choices:
            print("No media files found...")
            return None
        questions = [
            inquirer.List('file', message="Select a media file to upload", choices=file_choices),
        ]
        answers = inquirer.prompt(questions)
        if answers is None:
            print("Cancelled.")
            return None
        return answers['file']

    def loading_spinner(stop_event):
        spinner = ['|', '/', '-', '\\', '◜', '◞', '◝', '◞', '◟', '◠', '◡']
        while not stop_event.is_set():
            for symbol in spinner:
                if stop_event.is_set():
                    break
                sys.stdout.write(f'\rUploading {symbol}       ')
                sys.stdout.flush()
                time.sleep(0.1)

    if file_path is None:
        file_path = choose_file()
        if file_path is None:
            return

    full_file_path = os.path.join(os.getcwd(), file_path)

    if not os.path.isfile(full_file_path):
        print(f"File '{file_path}' not found.")
        return

    stop_event = threading.Event()

    spinner_thread = threading.Thread(target=loading_spinner, args=(stop_event,))
    spinner_thread.daemon = True 
    spinner_thread.start()

    try:
        with open(full_file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            stop_event.set()
            spinner_thread.join()
            
            if response.status_code == 200:
                print("\rSuccess!                     ")
                response_data = response.json()
                print("File URL:", response_data['message'])
            else:
                print(f"\rFailed, error: {response.status_code}                     ")
    except Exception as e:
        stop_event.set()
        spinner_thread.join()
        print(f"\rFailed, error: {e}                     ")

def lastFM(api_key, username):
    BASE_URL = "https://ws.audioscrobbler.com/2.0/"

    def fetch_recent_tracks():
        try:
            params = {
                'method': 'user.getRecentTracks',
                'api_key': api_key,
                'user': username,
                'limit': 5,
                'format': 'json'
            }

            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()
            recent_tracks = data.get('recenttracks', {}).get('track', [])
            return recent_tracks
        except requests.exceptions.RequestException as e:
            print(f"Error fetching recent tracks: {e}")
            return None
        except ValueError as e:
            print(f"Error decoding JSON response: {e}")
            return None
        

    return fetch_recent_tracks()

        
# image stuff
def imageOpen(image_path):
    try:
        img = Image.open(image_path)
        img.show()
        return img
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to open image: {e}\033[0m")
        return None

def imageResize(img, width, height):
    try:
        resized_img = img.resize((width, height))
        resized_img.show()
        return resized_img
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to resize image: {e}\033[0m")
        return None
