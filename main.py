import time
import unittest
from audio_processing import AudioExtractor
from timer import Timer
from audio_analysis import AudioAnalyzer
from colorizer import normalize_frequency, normalize_volume
from stick_render import StickRenderer


def main() -> None:
    FRAMERATE = 44100
    NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND = 25
    frame_size = int(FRAMERATE / NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND)

    audio = AudioExtractor('audio_data3')
    analyzer = AudioAnalyzer(freq_mode='fourier', vol_mode="rms", framerate=FRAMERATE)
    time.sleep(0.75)  # for synchronization purposes
    timer = Timer()
    render = StickRenderer(number_of_windows=audio.get_number_of_tracks() )

    while True:
        time_elapsed = timer.get_elapsed()
        cur_wav_frame_index = audio.time_to_frame_index(time=time_elapsed)
        window = (cur_wav_frame_index, cur_wav_frame_index + frame_size)

        frames_for_each_track = audio.get_frames_for_each_track(frames_window=window)
        for i, frames in enumerate(frames_for_each_track):
            avg_volume = analyzer.estimate_volume(frames)
            normalized_avg_volume = normalize_volume(avg_volume)
            freq = analyzer.estimate_freq(frames)
            normalized_freq = normalize_frequency(freq, max_x=10000)
            render.set_stick_levels(left_level=normalized_avg_volume,
                                    right_level=normalized_freq,
                                    window_number=i)
            print(f"#{i}: Average Volume: {avg_volume}, Average Frequency: {freq}")
        render.update()


if __name__ == '__main__':
    main()
