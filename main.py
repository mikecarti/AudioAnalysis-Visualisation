import unittest
from audio_processing import AudioExtractor
from timer import Timer
from audio_analysis import AudioAnalyzer
from render import Renderer

def main() -> None:
    FRAMERATE = 44100
    NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND = 50
    frame_size = int(FRAMERATE / NUM_OF_CONSEQUENT_WINDOWS_PER_SECOND)

    audio = AudioExtractor('audio_data')
    analyzer = AudioAnalyzer(freq_mode='fourier', framerate=FRAMERATE)
    timer = Timer()
    renderer = Renderer()

    while True:
        time_elapsed = timer.get_elapsed()
        cur_wav_frame_index = audio.time_to_frame_index(time=time_elapsed)
        window = (cur_wav_frame_index, cur_wav_frame_index + frame_size)
        frames = audio.get_frames_from_range(frames_window=window)
        avg_volume = analyzer.estimate_volume(frames)
        freq = analyzer.estimate_freq(frames)
        print(f"Average Volume: {avg_volume}, Average Frequency: {freq}")

if __name__ == '__main__':
    main()