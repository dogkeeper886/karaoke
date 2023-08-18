import pyaudio
import threading

# Global variable to track keyboard input
exit_flag = False

def handle_input():
    global exit_flag
    while True:
        user_input = input("Press 'q' to quit: ")
        if user_input == 'q':
            exit_flag = True
            break

def pass_audio():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open microphone stream
    mic_stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

    # Open speaker stream
    speaker_stream = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                output=True)
    
    # Start handling input in a separate thread
    input_thread = threading.Thread(target=handle_input)
    input_thread.start()

    # Pass audio from microphone to speaker
    while not exit_flag:
        data = mic_stream.read(1024)
        speaker_stream.write(data, 1024)

    # Stop and close streams
    mic_stream.stop_stream()
    mic_stream.close()
    speaker_stream.stop_stream()
    speaker_stream.close()
    audio.terminate()

if __name__ == '__main__':
    pass_audio()