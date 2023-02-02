from queue import Queue
from threading import Thread
from tqdm import tqdm
from math import floor


def reader(pipe, queue):
    try:
        with pipe:
            for line in iter(pipe.readline, b''):
                queue.put((pipe, line))
    finally:
        queue.put(None)

# Progress Bar by Gulski from https://github.com/kkroening/ffmpeg-python/issues/43#issuecomment-924800648
def progress_bar(process, total_duration):
    q = Queue()
    error = ''
    Thread(target=reader, args=[process.stdout, q]).start()
    Thread(target=reader, args=[process.stderr, q]).start()
    bar = tqdm(total=round(total_duration, 2))
    for _ in range(2):
        for source, line in iter(q.get, None):
            line = line.decode()
            if source == process.stderr:
                error = ' '
                # error += line
            else:
                line = line.rstrip()
                parts = line.split('=')
                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None
                if key == 'out_time_ms':
                    time = max(round(float(value) / 1000000., 2), 0)
                    bar.update(floor(time - bar.n))
                elif key == 'progress' and value == 'end':
                    bar.update(bar.total - bar.n)
    bar.close()
    return f'FFmpeg warning or error, perhaps the input was incorrect.\n\n{error}' if error else 'The media processing was successful.\n'

