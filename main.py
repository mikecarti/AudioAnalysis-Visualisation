import time
import unittest
from audio_processing import AudioExtractor
from timer import Timer
from audio_analysis import AudioAnalyzer
from colorizer import normalize_frequency, normalize_volume, get_color
from circle_render import Renderer


def main() -> None:
    FRAMERATE = 44100
    NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND = 25
    frame_size = int(FRAMERATE / NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND)

    audio = AudioExtractor('audio_data1')
    analyzer = AudioAnalyzer(freq_mode='fourier', vol_mode="rms", framerate=FRAMERATE)
    time.sleep(0.9)  # for synchronization purposes
    timer = Timer()
    render = Renderer(n_of_objects=audio.get_number_of_tracks())

    while True:
        time_elapsed = timer.get_elapsed()
        cur_wav_frame_index = audio.time_to_frame_index(time=time_elapsed)
        window = (cur_wav_frame_index, cur_wav_frame_index + frame_size)

        frames_for_each_track = audio.get_frames_for_each_track(frames_window=window)
        render.prepare_screen( )

        for i, frames in enumerate(frames_for_each_track):
            avg_volume = analyzer.estimate_volume(frames)
            normalized_avg_volume = normalize_volume(avg_volume)
            freq = analyzer.estimate_freq(frames)
            normalized_freq = normalize_frequency(freq, max_x=1000)
            render.move_object(speed=normalized_avg_volume,
                                    color=get_color(normalized_freq),
                                    object_number=i)
            print(f"#{i}: Average Volume: {avg_volume}, Average Frequency: {freq}")
        render.update()


if __name__ == '__main__':
    main()
