import unittest
from time import sleep

from audio_processing import AudioExtractor
from timer import Timer
from audio_analysis import AudioAnalyzer
from colorizer import *
from circle_render import Renderer


class TestAudioExtractor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        audio = AudioExtractor('audio_data1')
        audio.quit()
        cls.audio = audio

    def test_extractor_read_data_from_folder_and_data_existed(self):
        feats = self.audio.features
        self.assertIsNotNone(feats)

    def test_can_take_window_time_range_from_extractor(self):
        window = (9894, 44100)
        frames = self.audio.get_frames_from_range(frames_window=window)
        self.assertTrue(len(frames) == window[1] - window[0])
        self.assertTrue(type(frames) == np.ndarray)

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
        f = AudioAnalyzer(freq_mode="fourier", vol_mode="", framerate=frate)
        frames = [-2, 2] * (frate // 2)
        estimated_frequency = f.estimate_freq(frames)
        self.assertEqual(estimated_frequency, frate // 2)

        frames = [-2, -1, 2] * (frate // 3)
        estimated_frequency = f.estimate_freq(frames)
        self.assertEqual(estimated_frequency, frate // 3)

    def test_simple_vol_estimator(self):
        frate = 44100
        f = AudioAnalyzer(freq_mode="", vol_mode="simple", framerate=frate)
        frames = [0, 2] * (frate // 2)
        estimated_volume = f.estimate_volume(frames)
        self.assertEqual(estimated_volume, 1)


class TestRenderer(unittest.TestCase):
    def test_init(self):
        s = Renderer()


class TestColorizer(unittest.TestCase):
    def test_normalizer_0_1(self):
        a = 1123412525
        self.assertTrue(0 <= normalize(a, min_x=0, max_x=10 ** 12) <= 1)

    def test_get_color(self):
        col = get_color(0.5)
        self.assertTrue(len(col) == 3)
        self.assertTrue(type(col) is list)
        print("Color:", col)

    def test_number_to_normalized(self):
        norm = normalize(4252525, min_x=0, max_x=10 ** 8)
        self.assertTrue(0 <= norm <= 1)


class TestStickRender(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.renderer = Renderer()

    def test_draw_line(self):
        pos_1 = (0, 0)
        pos_2 = (50, 50)
        self.renderer.draw_line(pos_1, pos_2)
        sleep(2)

    def test_set_levels(self):
        self.renderer.set_stick_levels(0.5, 0.1)

if __name__ == '__main__':
    unittest.main()
