import os

# file operations and more
def write(file_name, mode, content):
    try:
        with open(file_name, mode) as file:
            file.write(content)
        return True
    except IOError as e:
        print(f"[ERROR] Failed to write to file: {e}")
        return False

def read(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"[ERROR] Failed to read file: {e}")
        return ""
      
def append(file_name, content):
    return write(file_name, 'a', content)

def file_exists(file_name):
    return os.path.exists(file_name)

def get_file_size(file_name):
    try:
        return os.path.getsize(file_name)
    except OSError as e:
        print(f"[ERROR] Failed to get file size: {e}")
        return -1

def delete_file(file_name):
    try:
        os.remove(file_name)
        return True
    except OSError as e:
        print(f"[ERROR] Failed to delete file: {e}")
        return False
        
def rename(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return True
    except OSError as e:
        print(f"[ERROR] Failed to rename file: {e}")
        return False


# python commands
def printPy(message):
    print(message)

def inputPy(prompt):
    return input(prompt)

def execPy(code):
    try:
        exec(code)
    except Exception as e:
        print(f"[ERROR] Failed to execute code: {e}")
