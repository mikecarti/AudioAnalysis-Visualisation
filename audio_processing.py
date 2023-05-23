import os
import numpy as np
import pandas as pd
import pyaudio
import wave
import threading
import math
from scipy.io.wavfile import read
from os.path import join as join_path
from typing import Dict
from time import sleep


class AudioExtractor:
    def __init__(self, audio_path):
        self.quiting = False
        self.stream = None
        self.framerate = None
        self.audio_dir = join_path(os.curdir, audio_path)
        self.features = self.collect_trackout()
        # for case of one wav file in audio folder
        self.decoded_wave = list(self.features.values())[0]
        self.player = pyaudio.PyAudio()

        self.test_features()
        self.test_wave = list(self.features.values())[0]

        self.play_audio()

    def collect_trackout(self) -> Dict:
        audio_dir = self.audio_dir
        # frames = {('name1': series1), ('name2': series2), ('name3': series3)}
        frames = {}
        framerates = set()
        for file_name in os.listdir(audio_dir):
            path = join_path(audio_dir, file_name)
            wave_frames = Wave.wav_to_series(path)
            framerates.add(Wave.get_framerate(path))
            frames[file_name] = wave_frames

        assert len(framerates) == 1, f"There are different framerates for this trackout: {framerates}"
        self.framerate = framerates.pop()

        # frames_df = self.convert_index_to_timestamps( pd.DataFrame(frames) )
        return frames

    def test_features(self):
        for col_name in self.features.keys():
            print(col_name)

    def play_audio(self):
        # define stream chunk
        chunk = 1024

        # open a wav format music
        f = wave.open(r"./audio_data/sine.wav", "rb")
        # get PyAudio instance
        p = self.player
        # open stream
        self.stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                             channels=f.getnchannels(),
                             rate=f.getframerate(),
                             output=True)
        # read data
        data = f.readframes(chunk)

        def play_stream(data, chunk):
            while not self.quiting and data:
                self.stream.write(data)
                data = f.readframes(chunk)

        thr = threading.Thread(target=play_stream, args=(data, chunk), kwargs={})
        thr.start()

    def get_frames_from_range(self, frames_window: tuple):
        if frames_window[0] < 0 or frames_window[1] > len(self.decoded_wave):
            raise Exception("frame window out of range: " + str(frames_window))
        return self.decoded_wave[frames_window[0]:frames_window[1]]

    def quit(self):
        # stop stream
        self.quiting = True
        sleep(0.5)
        self.stream.stop_stream()
        self.stream.close()

        # close PyAudio
        self.player.terminate()

    def time_to_frame_index(self, time: float):
        return math.floor(time * self.framerate)

    def get_current_time_frames(self, time: float) -> Dict:
        frame_number = self.time_to_frame_index(time)
        cur_named_frames = {}
        for k, v in self.features.items():
            cur_frame = v[frame_number]
            cur_named_frames[k] = cur_frame
        return cur_named_frames

    def convert_index_to_timestamps(self, frames_df):
        """
        DEPRECATED
        :param frames_df:
        :return:
        """

        # so every second we have n = framerate frames going through stream
        # then n rows are placed between 0 and 1 second
        # then every row index may be represented as: time_in_seconds = row_number / framerate
        frames_df.index = np.vectorize(lambda idx: idx / self.framerate)(frames_df.index)
        print(frames_df.iloc[[44100]])

        return frames_df


class Wave:
    def __init__(self, samplerate, wav_frames):
        self.samplerate = samplerate
        self.wav_frames = wav_frames

    @staticmethod
    def get_framerate(path):
        samplerate, _ = read(path)
        # in a wave file it is true
        framerate = samplerate
        return framerate

    @staticmethod
    def stereo_to_mono(left_ch, right_ch):
        return np.add(left_ch / 2.0, right_ch / 2.0)

    @staticmethod
    def wav_to_series(wav_path, verbose=False):
        samplerate, data = read(wav_path)

        channel_num = data.shape[1]
        length = data.shape[0] / samplerate

        if verbose:
            print(wav_path)
            print(f"number of channels = {channel_num}")
            print(f"length = {length}s\n")

        if channel_num == 2:
            left_ch, right_ch = np.hsplit(data, 2)
            data = Wave.stereo_to_mono(left_ch, right_ch)

        frames_series = pd.Series(data.flatten())
        return frames_series
