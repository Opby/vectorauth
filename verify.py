from speechbrain.pretrained import SpeakerRecognition
#from speechbrain.pretrained import EncoderDecoderASR
import jellyfish
import wave
import sys
import json

from vosk import Model, KaldiRecognizer, SetLogLevel


#asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-transformer-transformerlm-librispeech", savedir="pretrained_models/asr-transformer-transformerlm-librispeech")
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
asr_model = Model(lang="en-us")

file1 = '/Users/Stevehe/Downloads/demo/speechbrain/to_be_verified.wav'
file2 = '/Users/Stevehe/Downloads/demo/speechbrain/to_be_verified.wav'

score, prediction = verification.verify_files(file1, file2)

print('raw score: ' + str(score))
print('verification result: ' + str(prediction.item()))

wf = wave.open(file1, "rb")

# initialize a str to hold results
results = ""
textResults = ""

rec = KaldiRecognizer(asr_model, wf.getframerate())
rec.SetWords(True)

secretphrase = "this is my secret phrase"

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

if (prediction.item()):
    #transcribed = asr_model.transcribe_file("/Users/Stevehe/Downloads/demo/wav/speechbrain/isaacouput.wav")
    #sim_score = jellyfish.jaro_similarity(transcribed, secretphrase)

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
            print ("rec.Results: " + textResults)

        else:
            recognizerResult = rec.PartialResult()
            results = recognizerResult
            # convert the recognizerResult string into a dictionary  
            resultDict = json.loads(recognizerResult)
            # save the 'text' value from the dictionary into a list
            if (len(resultDict.get("partial", "")) != 0):
                textResults = resultDict.get("partial", "")
            print ("rec.PartialResults: " + textResults)
            
    # process "final" result
    results = results + rec.FinalResult()
    resultDict = json.loads(rec.FinalResult())
    textResults = textResults + resultDict.get("text", "")
    print ("rec.FinalResults: " + textResults)

    sim_score = jellyfish.jaro_similarity(textResults, secretphrase)
    print ("transcribed: " + textResults)
    print (sim_score)


