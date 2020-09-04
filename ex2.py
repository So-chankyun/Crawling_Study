import os
import subprocess
import pytube
# "https://www.youtube.com/watch?v=4vf885ONT0w"
url = input("url 주소를 입력하세요 : ")
video = pytube.YouTube(url)

v = video.streams.filter(file_extension='mp4').all()

# 영상 형식 리스트 확인
for i in range(len(v)):
    print(i,'. ',v[i])

vnum = int(input("다운 받을 화질은?"))

parent_dir = "D:/video/"
v[vnum].download(parent_dir)
---
new_filename = input("변환할 mp3 파일명은?")

default_filename = v[vnum].default_filename

subprocess.call(['ffmpeg','-i' ,os.path.join(parent_dir,default_filename),os.path.join(parent_dir,new_filename)])

print("동영상 다운로드 및 mp3 변환 완료!")