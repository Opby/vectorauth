#!/usr/bin/python3 

import serial
import os
import subprocess
import sys
import time
import Quartz
from ctypes import CDLL
from piwho import recognition, vad
import pyaudio
import wave

#below section is to import necessary packages from SpeechBrain. Pre-req follow the instructions to install SpeechBrain
#required to run in root directory/speechbrain, otherwise speechbrain model will give error
#python3 -m pip xxx
from speechbrain.pretrained import SpeakerRecognition

#below section is to import necessary packages from VOSK. Pre-req follow the instructions to install VOSK
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import jellyfish 

#use speechbrain's speaker recognition model
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
#asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-transformer-transformerlm-librispeech", savedir="pretrained_models/asr-transformer-transformerlm-librispeech")

#use VOSK's ASR model - small, much better recognition latency
asr_model = Model(lang="en-us")

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 16000  # Record at 44100 samples per second
seconds = 3
filename = "to_be_verified.wav"

badge_ids = {
#    '920A' : 'Alicia',
    '920A' : 'isaac',
}

secretphrase = "this is my secret phrase"

def is_screen_locked():
    """ check if screen is currently locked """
    settings = Quartz.CGSessionCopyCurrentDictionary()
    return ("CGSSessionScreenIsLocked = 1" in settings)

def identify_voice(speaker):
    """ check if speaker's voice matches the record """
    # vad.record()
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print('verifying ' + speaker)
    file1 = '/Users/Stevehe/Downloads/demo/speechbrain/to_be_verified.wav'
    file2 = '/Users/Stevehe/Downloads/demo/speechbrain/isaacoutput.wav'

    score, prediction = verification.verify_files(file1, file2)

    print('raw score: ' + str(score))
    print('verification result: ' + str(prediction.item()))

    if prediction.item() is False:
        os.system("say 'Voice does not match, you are not " + name + "!'")

    sim_score = 0
    wf = wave.open(file1, "rb")

    # initialize a str to hold results
    results = ""
    textResults = ""
        
    if (prediction.item()):
        rec = KaldiRecognizer(asr_model, wf.getframerate())
        rec.SetWords(True)


        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                recognizerResult = rec.Result()
                results = results + recognizerResult
                # convert the recognizerResult string into a dictionary  
                resultDict = json.loads(recognizerResult)
                # save the 'text' value from the dictionary into a list
                textResults = textResults + resultDict.get("text", "")

            else:
                recognizerResult = rec.PartialResult()
                results = recognizerResult
                # convert the recognizerResult string into a dictionary  
                resultDict = json.loads(recognizerResult)
                # save the 'text' value from the dictionary into textResults
                if (len(resultDict.get("partial", "")) != 0):
                    textResults = resultDict.get("partial", "")
                print ("rec.PartialResults: " + textResults)
                
        # process "final" result
        results = results + rec.FinalResult()
        resultDict = json.loads(rec.FinalResult())
        textResults = textResults + resultDict.get("text", "")

        sim_score = jellyfish.jaro_similarity(textResults, secretphrase)
    
        print ("transcribed text is: " + textResults)
        print ("sim_score is: " + str(sim_score))
        #transcribed = asr_model.transcribe_file(file1) for speechbrain's ASR model
        if sim_score < 0.8:
            os.system("say '" + name + " your secret phrase is incorrect!'")
        
    
    return (prediction.item() and sim_score > 0.8)

def in_secure_area(locked, x, y, z):
    """ check if the given location is in the secure area 

              Coordinate system

       x               (0.4, 0)
     <---------------------------------------------- (0, 0)
                              |                    |
                              |      COMPUTER      |
                              |____________________| (0, 0.25)                        |
                                                   |
                                                   |
                                                  \|/  y
    """
    # calibrated model
    y = 1.24 * y + 0.15
    print("After calibration: x = " + str(x) + ", y = " + str(y))

    x_min = -0.5
    x_max = 1.0
    y_min = -0.5
    y_max = 1.0

    gray_space = 0.2
    if locked is True:
        return (x >= (x_min + gray_space) and x <= (x_max - gray_space) and y <= (y_max - gray_space) and y >= (y_min + gray_space))
    else:
        return (x >= x_min and x <= x_max and y <= y_max and y >= y_min)


# object for voice recognition from old model
#recog = recognition.SpeakerRecognizer('./')
#print(recog.get_speakers())

# object for locking screen
loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')

# connect to DWM listener node
DWM = serial.Serial(port="/dev/tty.usbmodem0007601808241", baudrate=115200)
print("Connected to " + DWM.name)
DWM.write("\r\r".encode())
print("Encoded")
#time.sleep(1)

# lep is a DWM command to start reporting position of the active tags in the network
DWM.write("lep\r".encode())
print("Encoded")
#time.sleep(1)

# get the initial state of the screen
locked = is_screen_locked()
print("ScreenIsLocked = " + str(locked))

os.system('say "Enter the system."')
try:
    while True:
        # read report from DWM board and parse the information
        #print ("reading UWB data")
        data = DWM.readline()
        #print ("read data " + str(data))
        if(data):
            #print(data)
            data = data.decode()
            # Expected output format from 'lep' command
            #   POS,0,18B9,2.57,2.00,1.67,97    (meaning: position, tag_node_index, tag_device_id, x, y, z, quality_factor)
            if ("POS" in data):
                data = data.replace("\r\n", "")
                data = data.split(",")
                id = data[2]
                quality_factor = int(data[6])
                if quality_factor > 80 and id in badge_ids:
                    print(data)
                    x = float(data[3])
                    y = float(data[4])
                    z = float(data[5])
                    
                    # map device ID to user name
                    name = badge_ids[data[2]]
                    print('check speaker ' + name)

                    # check if the current location is within the predefined secure area bounding box
                    dist_check = in_secure_area(locked, x, y, z)

                    if locked is True and dist_check is True:
                        print("Unlocking location: x = " + str(x) + " y = " + str(y))
                        os.system('say "You have entered the secure area, please speak to unlock the computer"')

                        # check if voice matches
                        voice_check = identify_voice(name)
                        if voice_check is True:
                            subprocess.call('./unlock_screen.csh', shell=True)
                            locked = False
                            os.system("say 'Hello, " + name + "!'")
                        else:
                            os.system("say 'please try again!'")
                    elif locked is False and dist_check is False:
                        print("Locking location: x = " + str(x) + " y = " + str(y))
                        os.system('say "' + name + ' is out of the secure area, locking the computer."')
                        # Lock screen
                        result = loginPF.SACLockScreenImmediate()
                        locked = True
                #print("quality_factor is too low: " + str(quality_factor) + " or id is wrong " + id)
            #print ("POS not in data" + str(data))
            DWM.flushInput()
        #print ("no valid data received")
        DWM.flushInput()
    DWM.write("\r".encode())
    DWM.close()

except KeyboardInterrupt:
    print("Stop")
    DWM.write("\r\r".encode())
    DWM.close()
except Exception as e:
    print(traceback.format_exc())
    DWM.write("\r\r".encode())
    DWM.close()

