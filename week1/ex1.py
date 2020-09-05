"""
첫 번째로 좌상단의 광고를 크롤링
두 번째로 우측의 광고를 크롤링
각 경우에 대해서 아래 세가지의 광고가 존재한다.

1. 배너가 이미지인 경우
   -> a태그의 id가 ac_banner_a이다.
일단은 하나의 iframe에 대해서만 크롤링을 해보도록 하자.
2. 배너가 동영상 및 이미지일 경우  
3. 애니메이션인 경우
4. 동영상일 경우
  -> video, class : rbp_video > poster(사진파일이다.)
  -> video 태그 아래
"""

import urllib
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://www.naver.com'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)

global i
i = 0

iframe_name = ['da_iframe_time','da_iframe_rolling']
div_name = ['image_area animation_start','rbp_video']

def div_crawling():
   global i
   try:
      isVideo = driver.find_element_by_name(div_name[1])
   except:
      # 애니메이션인 경우
      # 우선 class = image_area animation_start 인 div 태그를 찾는다.
      area = driver.find_element_by_name(div_name[0])
      # 각 img 태그의 src 속성값을 리스트로 저장한다.
      images = [img.get_attribute('src') for img in area.find_elements_by_xpath('./img')]
   
      # 각각의 의미지를 저장한다.
      for image in images:
         savename = 'naver_banner_'+str(i)+'.jpg'
         urllib.request.urlretrieve(image,savename)
         i+=1
   else:
      # 비디오인 경우
      if isVideo is not None:
         video = driver.find_element_by_class_name('video_area')
         poster_url = video.get_attrubute('poster')
         video_url = video.find_element_by_xpath('./video').get_attribute('src')
         savename_video = 'naver_banner_video.mp4'
         urllib.request.urlretrieve(video_url,savename_video)
      
      if poster_url is not None:
         savename_poster = 'naver_banner_poster.img'
         urllib.request.urlretrieve(poster_url,savename_poster)

def image_video():
    driver.switch_to_default_content()
    video = driver.find_element_by_class_name('video_area')
    image = driver.find_element_by_class_name('image_area')
    img_url = image.find_element_by_xpath('./img').get_attribute('src')
    video_url = video.find_element_by_xpath('./video').get_attribute('src')
    savename_img = 'naver_banner_img.jpg'
    savename_video = 'naver_banner_video.mp4'
    urllib.request.urlretrieve(img_url,savename_img)
    urllib.request.urlretrieve(video_url,savename_video)

def iframe_crawling(name):
   global i
   iframe = driver.find_element_by_id('ac_banner_a')
   url = iframe.find_element_by_xpath('./img').get_attribute('src')
   savename = 'naver_banner_'+str(i)+'.jpg'
   urllib.request.urlretrieve(url,savename)
   driver.switch_to_default_content()
   i+=1

def top_of_left():
   driver.switch_to_frame(iframe_name[0])
   try:
      driver.find_element_by_id('ac_banner_a')
   except:
      image_video()
   else:
      iframe_crawling(iframe_name[0])
      # iframe이 있는 경우 즉, 하나의 img태그를 갖고 있는 경우

def right():
   driver.switch_to_frame(iframe_name[1])
   try:
      driver.find_element_by_id('ac_banner_a')
   except:
   # 만약 해당 frame이 없는 경우 
   # 영상이거나, 애니메이션인 경우 없다.
   # 애니매이션 혹은 영상
      div_crawling()
   # 영상이거나 애니메이션열 경우의 함수를 호출
   else:
      iframe_crawling(iframe_name[1])
      # iframe이 있는 경우 즉, 하나의 img태그를 갖고 있는 경우

top_of_left()
right()
   
   







