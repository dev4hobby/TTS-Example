from settings import misc
from gtts import gTTS
from pydub import AudioSegment

import random
import os


class CustomTTS():
    result_sound = None
    lang = misc.get('lang') and misc.get('lang') or 'ko'
    random_factor = misc.get('random_factor') and misc.get(
        'random_factor') or 0.25
    normal_frame_rate = misc.get('normal_frame_rate') and misc.get(
        'normal_frame_rate') or 44100
    pitch = misc.get('pitch') and misc.get('pitch') or 2.0
    skip_whitespace_level = misc.get(
        'get_skip_whitespace_level') and misc.get('skip_whitespace_level') or 3

    def __init__(self, pitch=None, random_factor=None, skip_faster=None):
        os.makedirs(name='samples', exist_ok=True)
        os.makedirs(name='result', exist_ok=True)
        if pitch:
            self.pitch = pitch
        if random_factor:
            self.random_factor = random_factor
        if skip_faster:
            self.skip_whitespace_level = skip_faster

    def create_speech(self, sentence: str):
        for letter in sentence:
            if letter == ' ':  # if whitespace come
                new_sound = letter_sound._spawn(
                    b'\x00' * (self.normal_frame_rate //
                               (self.skip_whitespace_level * 3)),
                    overrides={'frame_rate': self.normal_frame_rate}
                )
            else:
                try:
                    if not os.path.isfile('samples/%s.mp3' % letter):
                        tts = gTTS(letter, lang=self.lang)
                        tts.save('samples/%s.mp3' % letter)

                    letter_sound = AudioSegment.from_mp3(
                        'samples/%s.mp3' % letter)

                    raw = letter_sound.raw_data[9000:-9000]

                    octaves = 2.0 + random.random() * self.random_factor
                    frame_rate = int(
                        letter_sound.frame_rate * (2.0 ** octaves))
                    print('%s >> octaves: %.2f, frame rate: %.d' %
                          (letter, octaves, frame_rate))

                    new_sound = letter_sound._spawn(
                        raw,
                        overrides={'frame_rate': frame_rate}
                    )
                except Exception as e:
                    print('Error >> {}, {}'.format(letter, e))
                    continue
            new_sound = new_sound.set_frame_rate(self.normal_frame_rate)
            self.result_sound = new_sound if self.result_sound is None else self.result_sound + new_sound

        self.result_sound.export('result/%s.mp3' % sentence, format='mp3')
