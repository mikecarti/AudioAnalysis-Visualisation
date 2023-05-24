import unittest
import pandas as pd
from time import sleep

from audio_processing import AudioExtractor
from timer import Timer
from audio_analysis import AudioAnalyzer


class TestAudioExtractor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        audio = AudioExtractor('audio_data')
        audio.quit()
        cls.audio = audio

    def test_extractor_read_data_from_folder_and_data_existed(self):
        feats = self.audio.features
        self.assertIsNotNone(feats)

    def test_can_take_window_time_range_from_extractor(self):
        window = (9894, 44100)
        frames = self.audio.get_frames_from_range(frames_window=window)
        self.assertTrue(len(frames) == window[1] - window[0])
        self.assertTrue(type(frames) == pd.Series)

    def test_when_window_is_out_of_bounds_raises_error(self):
        def error_catching(w):
            frames = self.audio.get_frames_from_range(frames_window=w)

        window = (-100, 3000)
        self.assertRaises(Exception, error_catching, window)
        window = (100, 10 ** 100)
        self.assertRaises(Exception, error_catching, window)


class TestTimer(unittest.TestCase):

    def test_check_time(self):
        timer = Timer()
        sleep(1)
        self.assertAlmostEqual(timer.get_elapsed(), 1, places=2)


class TestAudioAnalyzer(unittest.TestCase):
    def test_fft_freq_estimator(self):
        frate = 44100
        f = AudioAnalyzer(freq_mode="fourier", framerate=frate)
        frames = [-2, 2] * (frate // 2)
        estimated_frequency = f.estimate_freq(frames)
        self.assertEqual(estimated_frequency, frate // 2)

        frames = [-2, -1, 2] * (frate // 3)
        estimated_frequency = f.estimate_freq(frames)
        self.assertEqual(estimated_frequency, frate // 3)

    def test_vol_estimator(self):
        frate = 44100
        f = AudioAnalyzer(freq_mode="", framerate=frate)
        frames = [0, 2] * (frate // 2)
        estimated_volume = f.estimate_volume(frames)
        self.assertEqual(estimated_volume, 1)

if __name__ == '__main__':
    unittest.main()
