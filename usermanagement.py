#!/usr/bin/env python3

import os
import subprocess
import random
import crypt
import pwd

username = input("Input user name: ")

# Check if user exists
def exists(username):
    try:
        get = pwd.getpwnam(username)
        return True
    except KeyError:
        return False 

# Add user
def adduser(fullname, username):
    full = fullname.replace(" ","")
    password = ''.join(random.sample(full,len(full))) + str(random.randrange(1, 10, 2))
    encrypted = crypt.crypt(password,"22")
    
    generate = ["sudo", "useradd","-p", encrypted , "-c", full, username]

    if not exists(username):
        add = subprocess.Popen(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        output,error = add.communicate()

        if add.returncode == 0:
            print("Succesfully created user: {}".format(username))
            return True
        else:
            print(error.decode("utf-8"))
            return False
    else:
        print("User {} already exists!".format(username))

# Remove user
def removeuser(username):
    if exists(username):
       remove = subprocess.Popen(["sudo", "userdel", "-r" , username], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

       output,error = remove.communicate()
       if remove.returncode == 0:
            print("Sucessfully removed user: {}".format(username))
    else:
       print("User already deleted/doesnt exist!")

# Lock the account
def lock(username):
    if exists(username):
        lock = subprocess.Popen(["sudo", "passwd", "-l", username], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        output,error = lock.communicate()
        if lock.returncode == 0:
            print("Successfully locked user: {}".format(username))
        else:
            print(error.decode("utf-8"))

# Unlock the account
def unlock(username):
    if exists(username):
        unlock = subprocess.Popen(["sudo", "usermod", "-U", username], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        output,error = unlock.communicate()
        if unlock.returncode == 0:
            print("Succesfully unlocked user: {}".format(username))
        else:
            print(error.decode("utf-8"))

# change real name / full name associated with account
def change_fullname(username):
    new_fullname = input("Input new full name here: ").replace(" ","")
    get = pwd.getpwnam(username)
    fullname = ''.join(get[4].split(","))
    change = subprocess.Popen(["sudo","chfn", "-f",  new_fullname, username], stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    
    output,error = change.communicate()
    if change.returncode == 0:
        print("Succesfully changed name from {} to {}".format(fullname, new_fullname))
    else:
        print(error.decode("utf-8"))


# ----MENU----

choices = ["create","delete","modify"]

prompt = int(input("Choose option: 0 for create, 1 for delete, 2 for modify: "))

if prompt in range(0,3):
    if choices[prompt] == "create":
        adduser(input("Input full name here: "), username)
    elif choices[prompt] == "delete":
        removeuser(username)
    else:
        modifyoptions = int(input("Choose option: 0 for lock user, 1 for unlock user, 2 for change real name/full name: "))
        if modifyoptions == 0:
            lock(username)
        elif modifyoptions == 1:
            unlock(username)
        elif modifyoptions == 2:
            change_fullname(username)
