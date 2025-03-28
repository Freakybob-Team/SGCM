import os
import platform
import json
import shutil
import datetime
import base64
import requests
import urllib.parse

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
        with open(file_name, mode) as file:
            if isinstance(content, dict) or isinstance(content, list):
                content = json.dumps(content, indent=4)
            file.write(content)
        return True
    except IOError as e:
        print(f"\033[31m[ERROR] Failed to write to file: {e}\033[0m")
        return False


def read(file_name):
    try:
        with open(file_name, "r") as file:
            return file.read()
    except IOError as e:
        print(f"\033[31m[ERROR] Failed to read file: {e}\033[0m")
        return ""


def append(file_name, content):
    return write(file_name, "a", content)


def fileExists(file_name):
    return os.path.exists(file_name)


def fileSize(file_name):
    try:
        return os.path.getsize(file_name)
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to get file size: {e}\033[0m")
        return -1


def deleteFile(file_name):
    try:
        os.remove(file_name)
        return True
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to delete file: {e}\033[0m")
        return False


def rename(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return True
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to rename file: {e}\033[0m")
        return False


def fileCopy(src, dest):
    try:
        shutil.copy(src, dest)
        return True
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to copy file: {e}\033[0m")
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


def list_directory(directory):
    try:
        return os.listdir(directory)
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to list directory: {e}\033[0m")
        return []


# dictionary stuff
def dictionaryCreate(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except OSError as e:
        print(f"\033[31m[ERROR] Failed to create directory: {e}\033[0m")
        return False


def directoryExists(directory):
    return os.path.isdir(directory)


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
        print(f"[ERROR] Base64 encoding failed: {e}")
        return ""


def base64Decode(encoded_text):
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode("utf-8")
    except Exception as e:
        print(f"[ERROR] Base64 decoding failed: {e}")
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
            print(f"[ERROR] GET request failed with status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[ERROR] HTTP GET request failed: {e}")
        return None

def httpPost(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] POST request failed with status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[ERROR] HTTP POST request failed: {e}")
        return None

def urlEncode(text):
    return urllib.parse.quote(text)

def urlDecode(encoded_text):
    return urllib.parse.unquote(encoded_text)
