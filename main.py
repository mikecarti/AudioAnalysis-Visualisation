import unittest
from audio_processing import AudioExtractor
from timer import Timer
import numpy as np

def main() -> None:
    audio = AudioExtractor('audio_data')
    timer = Timer()
    frame_size = int(44100 / 50)
    while True:
        time_elapsed = timer.get_elapsed()
        cur_wav_frame_index = audio.time_to_frame_index(time=time_elapsed)
        window = (cur_wav_frame_index, cur_wav_frame_index + frame_size)

        frames = audio.get_frames_from_range(frames_window=window)
        print(np.mean(frames))

if __name__ == '__main__':
    main()