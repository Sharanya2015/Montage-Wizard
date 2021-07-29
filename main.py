import time
import cv2 as cv2
import easyocr
from datetime import datetime
from PIL import Image
import os, re, os.path
import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

reader = easyocr.Reader(['ch_sim','en'])

current_frame = 0
frame_check_rate = 60
start_minus = 15
end_plus = 15
result_list = []
left = 600
top = 600
right = 1200
bottom = 900
is_clip = False
start_time = 0
latest_knockdown_time = 0

#scan the download directory for video file
filename = "shiv.mkv"
cam = cv2.VideoCapture(filename)

#read the video file
while(True):
	ret, frame = cam.read()
	if ret:
		print("read a frame")
		name = str(current_frame) + '.jpg'
		if(current_frame%frame_check_rate == 0):
			print("current frame is nth frame")
			status = cv2.imwrite(name,frame)
			im = Image.open(name)
			im1 = im.crop((left, top , right, bottom))
			im1 = im1.save(name)
			result = reader.readtext(name, detail =0)
			curr_time = cam.get(cv2.CAP_PROP_POS_MSEC)/1000
			result_list.append(result) #I dont think we need this anymore
			
			os.remove(name)  #delete the saved file 
			
			for res in result:
				if "KNOCK" in res or "KOCK" in res or "NATED" in res or "ELMI" in res or "ASS" in res or "IST" in res or "KNU" in res or "DOwN" in res or "ELM" in res or "EUM" in res:
					print('knocked!!!' + str(curr_time))
					latest_knockdown_time = curr_time
					if(is_clip == False):
						print("is clip is false")
						start_time = curr_time
						is_clip = True
			if(is_clip):
				if((curr_time - latest_knockdown_time) >= 25):
					end_time = latest_knockdown_time + end_plus
					start_time = start_time - start_minus
					print("making a clip from" + str(start_time) + "_" + str(end_time))
					#TODO: change it later
					clipname = "Knock_" +str(start_time) + "_" + str(end_time) +".mp4"
					ffmpeg_extract_subclip(filename, start_time, end_time, targetname = clipname) 
					is_clip = False
		current_frame += 1
	else:
		print("Good Job, reading all the frames is complete")

		if(is_clip):
			end_time = latest_knockdown_time + end_plus
			start_time = start_time -start_minus
			print("Generating one more clip")
			filename = "Knock_" + str(start_time) +"_"+ str(end_time) + ".mp4"
			ffmpeg_extract_subclip(filename,start_time,end_time,targetname=clipname)
			break
		break


						

