from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import numpy as np
import aubio
import io
import wave
from pydub import AudioSegment

async_mode = None
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins=['https://mxweidmer-default-usfca.dev.8thwall.app'])

@socketio.on('hello')
def hello(message):
    print(message['data'])

# samplerate = 44100
# a_tempo = aubio.tempo("default", 1024, 1024 // 2, samplerate)
#
# @socketio.on('audio_chunk')
# def handle_audio_chunk(data):
#     remainder = len(data) % 4
#     clean_data = data
#     if remainder > 0:
#         clean_data = data[:-remainder]
#
#     samples = np.frombuffer(clean_data, dtype=np.float32)
#
#     frame_size = 1024
#     hop_size = 512
#
#     num_frames = len(samples) // hop_size
#
#     # Initialize an empty array to store the frames
#     frames = np.zeros((num_frames, hop_size), dtype=np.float32)
#
#     # Fill the frames array with overlapping segments from the original audio samples
#     for i in range(num_frames):
#         start = i * hop_size
#         end = start + hop_size
#         frames[i, :] = samples[start:end]
#
#     for frame in frames:
#         is_beat = a_tempo(frame)
#         print(is_beat)
#         if is_beat:
#             print('Beat detected!')

wave_file = None
wave_name = None

@socketio.on('start')
def handle_start():
    global wave_file, wave_name
    wave_name = 'out.wav'
    wave_file = wave.open(wave_name, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(44100)

@socketio.on('write_audio')
def handle_audio_chunk(data):
    global wave_file
    wave_file.writeframes(data)
    print('WAV file size:', wave_file.getnframes())

@socketio.on('audio_end')
def handle_audio_end():
    global wave_file, wave_name
    if wave_file is not None:
        wave_file.close()
        wave_file = None
        wave_name = None

if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=8080)