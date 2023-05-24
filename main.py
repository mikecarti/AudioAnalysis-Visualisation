import time
import unittest
from audio_processing import AudioExtractor
from timer import Timer
from audio_analysis import AudioAnalyzer
from render import Renderer
from colorizer import frequency_to_color, volume_to_color


def main() -> None:
    FRAMERATE = 44100
    NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND = 25
    frame_size = int(FRAMERATE / NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND)

    audio = AudioExtractor('audio_data')
    analyzer = AudioAnalyzer(freq_mode='fourier', vol_mode="rms", framerate=FRAMERATE)
    time.sleep(0.75)  # for synchronization purposes
    timer = Timer()
    renderer = Renderer()

    # max_vol = 0
    # max_freq = 0

    while True:
        time_elapsed = timer.get_elapsed()
        cur_wav_frame_index = audio.time_to_frame_index(time=time_elapsed)
        window = (cur_wav_frame_index, cur_wav_frame_index + frame_size)
        frames = audio.get_frames_from_range(frames_window=window)
        avg_volume = analyzer.estimate_volume(frames)
        freq = analyzer.estimate_freq(frames)

        renderer.change_left_color(volume_to_color(avg_volume))
        renderer.change_right_color(frequency_to_color(freq, max_freq=2000))

        print(f"Average Volume: {avg_volume}, Average Frequency: {freq}")


if __name__ == '__main__':
    main()
