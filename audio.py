import pyaudio
import ffmpeg
import time
# PyAudio有两种模式，一种是阻塞模式，一种是回调模式。
# 这里的场景应该使用回调模式，PyAudio主动请求音频数据，从而一定程度是缓解RTSP流的网络抖动。
# define callback (2)
def callback(in_data, frame_count, time_info, status):
    if process.poll() is None:
        #这里的2*frame_count中的2表示输入的音频是2字节即16bits编码
        data = process.stdout.read(2*frame_count)
        return (data, pyaudio.paContinue)

if __name__ == "__main__":
    # 子进程
    process = (
        ffmpeg
        .input('rtmp://localhost:1935/live/test')['a']
            # '-'将流输出至标准输出
            .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
            # 将子进程的标准输出由管道转出
            .run_async(pipe_stdout=True)
    )
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    output=True,
                    stream_callback=callback)
    # start the stream (4)
    stream.start_stream()
    # wait for stream to finish (5)
    while stream.is_active():
        time.sleep(0.1)
    # stop stream (6)
    stream.stop_stream()
    stream.close()
    process.terminate()
    # close PyAudio (7)
    p.terminate()