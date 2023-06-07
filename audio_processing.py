import os
import numpy as np
import pandas as pd
import pyaudio
import wave
import threading
import math
from scipy.io.wavfile import read
from os.path import join as join_path
from typing import *
from time import sleep


class AudioExtractor:
    def __init__(self, audio_path):
        self.quiting = False
        self.stream = None
        self.framerate = None
        self.audio_file_path = None
        self.audio_dir = join_path(os.curdir, audio_path)
        self.features = self.collect_trackout()
        # for case of one wav file in audio folder
        self.decoded_wave = list(self.features.values())[0]
        self.player = pyaudio.PyAudio()

        self.test_features()
        self.test_wave = list(self.features.values())[0]

        self.play_audio(file_names=list(self.features.keys()))

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

    def play_audio(self, file_names):
        # define stream chunk
        chunk = 1024
        paths = []
        waves = []
        streams = []
        data_waves = []
        print("File names: " + str(file_names))
        for file_name in file_names:
            paths.append(join_path(self.audio_dir, file_name))
        for path in paths:
            waves.append(wave.open(path, "rb"))

        # get PyAudio instance
        p = self.player
        # open stream
        for w in waves:
            streams.append(
                p.open(format=p.get_format_from_width(w.getsampwidth()),
                       channels=w.getnchannels(),
                       rate=w.getframerate(),
                       output=True)
            )
            data_waves.append(w.readframes(chunk))

        # read data
        def play_stream(data_waves, waves, streams, chunk):
            while not self.quiting and data_waves[0]:
                for i in range(len(data_waves)):
                    data = data_waves[i]
                    wave_file = waves[i]
                    streams[i].write(data)
                    data_waves[i] = wave_file.readframes(chunk)

        thr = threading.Thread(target=play_stream, args=(data_waves, waves, streams, chunk), kwargs={})
        thr.start()

    def get_number_of_tracks(self):
        return len(self.features.values())

    def get_frames_from_range(self, frames_window: tuple, decoded_wave: pd.Series) -> np.ndarray:
        if frames_window[0] < 0 or frames_window[1] > len(decoded_wave):
            raise Exception("frame window out of range: " + str(frames_window))
        return decoded_wave[frames_window[0]:frames_window[1]].to_numpy()

    def get_frames_for_each_track(self, frames_window: tuple) -> List[np.ndarray]:
        frames_for_each_track = list()
        for decoded_wave in list(self.features.values()):
            frames_for_each_track.append(self.get_frames_from_range(frames_window, decoded_wave))
        return frames_for_each_track

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


