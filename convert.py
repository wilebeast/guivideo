# -*- coding: utf-8 -*-
import os
import sys
import ffmpeg
import cv2
from moviepy.editor import AudioFileClip


# 提取音频
def get_audio_file(orig_video_file_name):
    index = orig_video_file_name.rfind(".mp4")
    audio_file_name = orig_video_file_name[0:index] + ".wav"
    my_audio_clip = AudioFileClip(orig_video_file_name)
    my_audio_clip.write_audiofile(audio_file_name)
    return audio_file_name


# 提取视频，并做视频帧提取操作
def get_tmp_video_file(orig_video_file_name, tmp_video_file_name):
    video = cv2.VideoCapture(orig_video_file_name)
    fps = video.get(cv2.CAP_PROP_FPS)
    frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    videoWriter = cv2.VideoWriter(tmp_video_file_name, cv2.VideoWriter_fourcc(*'MP4V'), fps, size)
    success, frame = video.read()
    index = 1
    while success:
        # 5帧取4帧
        # 这个逻辑可以根据实际情况做灵活调整
        if index % 5 != 0:
            # cv2.putText(frame, 'fps: ' + str(fps), (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 5)
            # cv2.putText(frame, 'count: ' + str(frameCount), (0, 300), cv2.FONT_HERSHEY_SIMPLEX,2, (255,0,255), 5)
            # cv2.putText(frame, 'frame: ' + str(index), (0, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 5)
            # cv2.putText(frame, 'time: ' + str(round(index / 24.0, 2)) + "s", (0,500), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 5)
            # cv2.imshow("new video", frame)
            # cv2.waitKey(1000 // int(fps))

            videoWriter.write(frame)
            success, frame = video.read()
        index += 1
    video.release()
    return tmp_video_file_name


# 合并视频、音频
def combine_video_and_audoi(tmp_video_file_name, audio_file_name):
    input_video = ffmpeg.input(tmp_video_file_name)
    input_audio = ffmpeg.input(audio_file_name)
    output_video_file_name = tmp_video_file_name.replace("tmp_", "new_")
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_video_file_name).run()


def start_convert(orig_video_file: str):
    audio_file_name = get_audio_file(orig_video_file)
    path, filename = os.path.split(orig_video_file)
    if path:
        path += "/"
    tmp_video_file_name = path + "tmp_" + filename
    get_tmp_video_file(orig_video_file, tmp_video_file_name)
    combine_video_and_audoi(tmp_video_file_name, audio_file_name)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage %s orig_video_file_name" % sys.argv[0])
        sys.exit(1)

    orig_video_file_name = sys.argv[1]
    audio_file_name = get_audio_file(orig_video_file_name)
    path, filename = os.path.split(orig_video_file_name)
    tmp_video_file_name = path + "tmp_" + filename
    get_tmp_video_file(orig_video_file_name, tmp_video_file_name)
    combine_video_and_audoi(tmp_video_file_name, audio_file_name)
