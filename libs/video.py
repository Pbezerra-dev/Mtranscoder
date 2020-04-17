from itertools import count
import os

from .check_files import files_exists
from .progresss_bar import progressbar


class Video:

    def __init__(
            self, input_midia_format: str, source_path: str, output_midia_format: str,
            output_path: str, bitrate: str, time: str, qrange: str) -> str:

        self.output_midia_format = output_midia_format
        self.input_midia_format = input_midia_format
        self.codec_video = '-c:v libx264'
        self.codec_audio = '-c:a aac'
        self.crf = '-crf 20'
        self.preset = '-preset ultrafast'
        self.bitrate_audio = bitrate
        self.command_ffmpeg = 'ffmpeg'
        self.time = ''
        self.source_path = source_path
        self.output_path = output_path
        self.time = time
        self.qrange = qrange

        if self.input_midia_format == 'webm' or output_midia_format == 'webm':
            self.codec_video = '-c:v vp9'
            self.codec_audio = '-c:a libvorbis'
        if self.input_midia_format == 'vob' or output_midia_format == 'vob':
            self.codec_audio = '-c:a ac3'

    def execute_files(self):
        files = set((files for files in os.listdir(self.source_path)[:self.qrange]
                     if self.input_midia_format in files.split('.')[-1]))
        print(files)
        if files:
            for file in files:
                name_file, extension_file = os.path.splitext(file)

                caption_path = name_file + '.srt'

                if os.path.isfile(caption_path):
                    caption_input = f'-i "{caption_path}"'
                    caption_map = '-c:s -map v:0 -map a -map 1:0'
                else:
                    caption_input = ''
                    caption_map = ''

                exit_file = (
                    f'{self.output_path}/{name_file}_{self.output_midia_format}.'
                    f'{self.output_midia_format}'
                )
                if files_exists(name_file, exit_file, self.output_midia_format):
                    command = (
                        f'{self.command_ffmpeg} -i "{self.source_path}/{file}" {caption_input} '
                        f'{self.codec_video} {self.crf} {self.preset} {self.codec_audio} '
                        f'{self.bitrate_audio} {self.time} {caption_map} "{exit_file}" -y'
                        f' &> /dev/null'
                    )

                    def ffmpeg():
                        if os.system(command):
                            for i in count(1):
                                ...
                        return

                    progressbar(ffmpeg)
                else:
                    break
        else:
            print(
                f'\nFiles with extension .{self.input_midia_format} in "{self.source_path}"')
