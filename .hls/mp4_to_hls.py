import ffmpeg_streaming
from ffmpeg_streaming import Formats, FFProbe
# memo : ffmpeg_streamingは、ホストマシンのffprobeのラッパー。
import os
import yf_upload
import shutil
from tqdm import tqdm
import quick_drop
from termcolor import cprint
import ffmpeg

api_url = 'http://127.0.0.1:5000/api/pypost_test'
api_register = 'http://127.0.0.1:5000/api/pypost_rdb'

def monitor(ffmpeg, duration:int, time_:int, time_left:int, process):
    t.update()
    t.total=duration
    t.n=time_

def mp4_to_hls(input_path:str):
    output_path = output_dir + '/stream.m3u8'

    video = ffmpeg_streaming.input(input_path)
    hls = video.hls(Formats.h264())
    hls.auto_generate_representations()
    hls.output(output_path, monitor=monitor)

def get_files_size(paths: list[str]):
    total_size = 0
    for path in paths:
        total_size += os.stat(path).st_size
    return total_size

def set_metadata(path:str, username:str) -> dict:
    ffprobe = FFProbe(path)
    ffprobe.save_as_json(os.path.join(output_dir, 'probe.json'))
    video_format = ffprobe.format()
    duration = int(float(video_format.get('duration', 0))) # str > float > int
    json_data = {
        'duration': duration,
        'filename': os.path.splitext(os.path.basename(path))[0],
        'username': username,
        }
    return json_data

def set_temp_path(path:str, id:int=0, workdir:str=''):
    output_dir = workdir + '/processing-' + str(id)
    target_path = output_dir + '/temp.mp4'
    os.makedirs(output_dir, exist_ok=True)
    os.link(input_path, target_path)
    return target_path, output_dir

def create_thumbnail(filepath:str, width:int, thumb_output:str, frame:int=0):
    out, err = (
        ffmpeg
        .input(filepath)
        .filter('scale', width, -1)
        .output(thumb_output + '/thumb.webp', vframes=1)
        .run(quiet=True)
    )
    return out

class YfLogDraw:
    def __init__(self, print_message:str):
        self.message = print_message
    def __enter__(self):
        cprint(self.message)
    def __exit__(self,type,value,traceback):
        print('\u001B[1A]', end='')
        cprint('\r' + self.message, 'blue')
    def cprint_redraw(items: list[str], color:str):
        cprint('\u001B['+ str(len(items)) +'A', end='')
        for item in items:
            cprint(item, color)

if __name__ == '__main__':
    paths = quick_drop.get_filelist()
    size = get_files_size(paths)
    cprint( str(len(paths)) + ' file(s) selected.', 'blue')
    cprint('Size(Total) : ' + str(round(size/1024/1024, 1)) + ' MB', 'blue')
    
    for index, input_path in enumerate(paths):

        workdir = os.path.splitdrive(input_path)[0] + '/temp'
        temp_path, output_dir = set_temp_path(input_path, index, workdir=workdir)

        step = [
            '<'+ str(index+1) + '/' + str( len(paths) ) + '> ' + input_path,
            '[1/3] Encoding to HLS',
            '[2/3] Uploading to Server',
            '[3/3] Register to DB'
        ]
        cprint(step[0], color='white')
        
        with YfLogDraw(step[1]):
            with tqdm(leave=False, desc='FFMPEG',colour='blue') as t:
                mp4_to_hls(temp_path)
                create_thumbnail(temp_path, width=400, thumb_output=output_dir)

        with YfLogDraw(step[2]):
            files = yf_upload.get_files(output_dir)
            yf_upload.uploads(files, api_url, input_path, username='yanagi55')
            
        with YfLogDraw(step[3]):
            json_data = set_metadata(input_path, username='yanagi55')
            yf_upload.register(json_data, api=api_register)

        YfLogDraw.cprint_redraw(step, 'blue')


    cprint('Complete : ' + str(paths), 'green')
    shutil.rmtree(workdir)