
# 파이썬 3.10 환경을 가져옵니다
FROM python:3.10-slim

# 영상 편집을 위한 필수 프로그램인 FFmpeg를 서버에 설치합니다
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# 작업 폴더를 설정합니다
WORKDIR /app

# 현재 폴더의 모든 파일을 서버로 복사합니다
COPY . /app

# 파이썬 필수 라이브러리들을 설치합니다
RUN pip install --no-cache-dir -r requirements.txt

# Render.com에서 서버를 실행하는 명령어입니다 (Gunicorn 사용)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "600", "server:app"]

from PIL import Image, ImageDraw, ImageFont
import os

def create_daily_image(template_path, new_text, output_path):
    # 템플릿 이미지가 없으면 임시로 생성 (실제 사용시에는 포토샵 등으로 글자가 없는 원본 템플릿을 만들어 'assets/template.jpg'로 저장해야 합니다)
    if not os.path.exists(template_path):
        img = Image.new('RGB', (1080, 1920), color = (240, 248, 255))
        d = ImageDraw.Draw(img)
        d.text((100, 100), "글자 없는 배경 템플릿을 추가해주세요.", fill=(255,0,0))
        img.save(template_path)
    
    # 템플릿 열기
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    
    # 폰트 설정 (윈도우 기본 폰트 사용, 굵은 폰트로 변경 권장)
    try:
        font = ImageFont.truetype("malgun.ttf", 60)
    except:
        font = ImageFont.load_default()

    # 이미지에 새로운 텍스트 덧그리기
    # 템플릿의 특정 좌표(x, y)에 새 글씨를 씁니다. 실제 디자인에 맞게 좌표 수정이 필요합니다.
    text_x, text_y = 150, 400 
    draw.text((text_x, text_y), new_text, font=font, fill=(0, 0, 0))
    
    # 완성된 이미지 저장
    img.save(output_path)

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoTube - 100% 무인 유튜브 영상 생산기</title>
    <style>
        body { font-family: 'Pretendard', sans-serif; background-color: #f4f7f6; color: #333; text-align: center; margin: 0; padding: 50px 20px;}
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto;}
        h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .btn-start { background-color: #fff; color: #764ba2; padding: 15px 40px; font-size: 1.2rem; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; transition: all 0.3s; margin-top: 20px;}
        .btn-start:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
        .btn-start:disabled { background-color: #ccc; color: #666; cursor: not-allowed; box-shadow: none; transform: none;}
        #status { margin-top: 20px; font-size: 1.1rem; font-weight: bold; color: #ffeb3b; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>AutoTube AI 웹 서비스</h1>
        <p>버튼 하나로 40일치 유튜브 영상 무인 생성 및 예약 업로드</p>
        <!-- 시작 버튼 -->
        <button id="startBtn" class="btn-start" onclick="startAutomation()">▶️ 40개 일괄 자동화 시작</button>
        <!-- 상태 표시줄 -->
        <p id="status"></p>
    </div>

    <script>
        // 백엔드 서버 주소를 여기에 입력해야 합니다 (예: Render.com에서 배포한 주소)
        const BACKEND_URL = "https://my-autotube-backend.onrender.com/start";

        async function startAutomation() {
            const btn = document.getElementById('startBtn');
            const status = document.getElementById('status');
            
            btn.disabled = true;
            btn.innerText = "작업 진행 중...";
            status.innerText = "공장에 작업 명령을 내렸습니다. (영상이 생성 중입니다...)";

            try {
                // 파이썬 백엔드로 시작 신호 보내기
                const response = await fetch(BACKEND_URL, { method: 'POST' });
                const data = await response.json();
                
                if(response.ok) {
                    status.innerText = "✅ 백엔드 공장에서 영상 생성을 성공적으로 시작했습니다!";
                } else {
                    status.innerText = "❌ 오류: " + data.message;
                    btn.disabled = false;
                    btn.innerText = "▶️ 40개 일괄 자동화 시작";
                }
            } catch (error) {
                status.innerText = "❌ 서버 연결 실패. 백엔드 서버가 켜져 있는지 확인하세요.";
                btn.disabled = false;
                btn.innerText = "▶️ 40개 일괄 자동화 시작";
            }
        }
    </script>
</body>
</html>

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoTube - 100% 무인 유튜브 영상 생산기</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
            background-color: #f4f7f6;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 50px 20px;
            text-align: center;
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 20px;
            border-radius: 20px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        p.subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        .btn-download {
            display: inline-block;
            background-color: #fff;
            color: #764ba2;
            padding: 15px 40px;
            font-size: 1.2rem;
            font-weight: bold;
            text-decoration: none;
            border-radius: 50px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .btn-download:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .features {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            text-align: left;
        }
        .feature-card {
            flex: 1;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }
        .feature-card h3 {
            color: #764ba2;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>AutoTube AI</h1>
            <p class="subtitle">단 한 번의 클릭으로 40일 치 유튜브 쇼츠 자동 생성 및 예약 업로드</p>
            <a href="#" class="btn-download">프로그램 다운로드 (app.exe)</a>
        </div>

        <div class="features">
            <div class="feature-card">
                <h3>⚡ 100% 무인 자동화</h3>
                <p>매달 신경 쓸 필요 없이 프로그램이 알아서 템플릿에 텍스트를 입히고 영상을 합성합니다.</p>
            </div>
            <div class="feature-card">
                <h3>📅 자동 예약 업로드</h3>
                <p>구글 API와 연동되어 내일부터 매일 하루에 하나씩 지정된 시간에 자동으로 채널에 공개됩니다.</p>
            </div>
            <div class="feature-card">
                <h3>🎨 템플릿 영구 유지</h3>
                <p>브랜드의 정체성을 담은 뼈대 이미지는 그대로 유지하면서 내용만 매일 새롭게 교체합니다.</p>
            </div>
        </div>
    </div>
</body>
</html>

import os
import datetime
from image_processor import create_daily_image
from video_maker import make_video
from youtube_uploader import get_authenticated_service, upload_video

# 40일치 영상 일괄 생성 및 예약 업로드
TOTAL_VIDEOS = 40
VIDEO_DURATION_SEC = 40

def main():
    print("🚀 유튜브 자동화 봇 실행 시작...")
    
    # 1. 유튜브 API 인증 (최초 1회만 브라우저 열림, 이후 토큰 재사용)
    youtube = get_authenticated_service()
    
    for i in range(TOTAL_VIDEOS):
        # 겹치지 않는 업로드 날짜 계산 (내일부터 하루에 하나씩)
        upload_date = datetime.datetime.now() + datetime.timedelta(days=i+1)
        
        # TODO: OpenAI API나 다른 방식을 통해 매일 다른 주제와 텍스트 생성 필요
        topic_title = f"2024년 성공 투자 전략 Part {i+1}"
        
        image_path = f"output/image_{i}.jpg"
        video_path = f"output/video_{i}.mp4"
        audio_path = "assets/bgm.mp3" # 저작권 무료 음악 필요
        
        # 2. 이미지 생성 (기본 틀 유지 + 텍스트 변경)
        print(f"[{i+1}/{TOTAL_VIDEOS}] 이미지 생성 중: {topic_title}")
        create_daily_image("assets/template.jpg", topic_title, image_path)
        
        # 3. 40초 영상 생성 (이미지 + 음악)
        print(f"[{i+1}/{TOTAL_VIDEOS}] 40초 영상 생성 중...")
        make_video(image_path, audio_path, video_path, VIDEO_DURATION_SEC)
        
        # 4. 유튜브 예약 업로드
        print(f"[{i+1}/{TOTAL_VIDEOS}] 유튜브 예약 업로드 중... (예약일: {upload_date.strftime('%Y-%m-%d')})")
        upload_video(youtube, video_path, topic_title, upload_date)
        
    print("✅ 작업이 끝났습니다!")

if __name__ == '__main__':
    # 폴더 준비
    os.makedirs('output', exist_ok=True)
    os.makedirs('assets', exist_ok=True)
    main()

Flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
Pillow==10.2.0
moviepy==1.0.3
google-api-python-client==2.118.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0

from flask import Flask, jsonify
from flask_cors import CORS
import threading
import os
import datetime
import pickle
import gc  # 메모리 청소를 위한 라이브러리
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = Flask(__name__)
CORS(app)

TOTAL_VIDEOS = 40
VIDEO_DURATION_SEC = 40
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def create_daily_image(template_path, new_text, output_path):
    if not os.path.exists(template_path):
        img = Image.new('RGB', (1080, 1920), color=(240, 248, 255))
        d = ImageDraw.Draw(img)
        d.text((100, 100), "No Template Found", fill=(255,0,0))
        img.save(template_path)
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("malgun.ttf", 60)
    except:
        font = ImageFont.load_default()
    draw.text((150, 400), new_text, font=font, fill=(0, 0, 0))
    img.save(output_path)

def make_video(image_path, audio_path, output_path, duration=40):
    if not os.path.exists(audio_path):
        from moviepy.audio.AudioClip import AudioArrayClip
        import numpy as np
        silence = AudioArrayClip(np.zeros((44100, 2)), fps=44100).set_duration(duration)
        silence.write_audiofile(audio_path, fps=44100, logger=None)
        
    img_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)
    if audio_clip.duration > duration:
        audio_clip = audio_clip.subclip(0, duration)
        
    video = img_clip.set_duration(duration).set_audio(audio_clip)
    # Render.com 메모리 제한을 위해 쓰레드를 1개로 제한하고 천천히 렌더링
    video.write_videofile(output_path, fps=1, codec="libx264", audio_codec="aac", logger=None, threads=1)
    
    # 작업이 끝난 클립들을 메모리에서 강제 해제 (서버 터짐 방지)
    img_clip.close()
    audio_clip.close()
    video.close()
    del img_clip, audio_clip, video
    gc.collect()

def get_authenticated_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return None
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, video_path, title, upload_date):
    publish_at = upload_date.isoformat() + '.000Z' 
    body = {
        'snippet': {
            'title': title,
            'description': '자동 생성된 금융 꿀팁 영상입니다.',
            'tags': ['재테크', '금융', '자동화'],
            'categoryId': '27'
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': publish_at,
            'selfDeclaredMadeForKids': False
        }
    }
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )
    insert_request.execute()

def run_automation_task():
    print("🚀 [서버 백그라운드] 40개 유튜브 영상 릴레이 자동화 시작")
    
    # 생성된 영상이 덮어씌워지지 않고 모두 저장되도록 날짜/시간별 폴더 생성
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_folder = f"output/작업물_{timestamp}"
    os.makedirs(save_folder, exist_ok=True)
    os.makedirs('assets', exist_ok=True)
    
    youtube = get_authenticated_service()
    if not youtube:
        print("⚠️ 유튜브 API 인증 정보(token.pickle)가 없습니다. 유튜브 업로드는 생략하고 파일만 저장합니다.")
        # return 하지 않고 파일 저장까지는 진행하도록 수정
        
    for i in range(TOTAL_VIDEOS):
        upload_date = datetime.datetime.now() + datetime.timedelta(days=i+1)
        topic_title = f"2024년 성공 투자 전략 Part {i+1}"
        image_path = f"{save_folder}/image_{i}.jpg"
        video_path = f"{save_folder}/video_{i}.mp4"
        audio_path = "assets/bgm.mp3"
        
        print(f"[{i+1}/{TOTAL_VIDEOS}] '{topic_title}' 생성 및 렌더링 중...")
        create_daily_image("assets/template.jpg", topic_title, image_path)
        
        # 하나씩 순차적으로 렌더링 진행
        make_video(image_path, audio_path, video_path, VIDEO_DURATION_SEC)
        
        if youtube:
            try:
                print(f"[{i+1}/{TOTAL_VIDEOS}] 유튜브 업로드 중...")
                upload_video(youtube, video_path, topic_title, upload_date)
                print(f"✅ 완료: {upload_date.strftime('%Y-%m-%d')} 예약됨")
            except Exception as e:
                print(f"❌ 업로드 실패: {e}")
        else:
            print(f"✅ 영상 제작 완료! (PC의 {save_folder} 폴더에 안전하게 저장되었습니다)")
            
        # 하나 끝날 때마다 메모리 완벽 청소
        gc.collect()
        
    print("🎉 [서버 백그라운드] 40개 영상 릴레이 작업이 모두 완료되었습니다!")

@app.route('/start', methods=['POST'])
def start_bot():
    """Netlify 웹페이지에서 버튼을 누르면 이 주소로 신호가 옵니다."""
    # 5분이 걸리든 10분이 걸리든 백그라운드에서 하나씩 릴레이로 작업하도록 던짐
    thread = threading.Thread(target=run_automation_task, daemon=True)
    thread.start()
    
    return jsonify({"status": "success", "message": "작업이 성공적으로 시작되었습니다! 백그라운드에서 순차적으로 진행됩니다."})

from moviepy.editor import ImageClip, AudioFileClip

def make_video(image_path, audio_path, output_path, duration=40):
    import os
    # 임시 오디오 파일 생성 (테스트용)
    if not os.path.exists(audio_path):
        from moviepy.audio.AudioClip import AudioArrayClip
        import numpy as np
        # 1초짜리 묵음 생성 후 길이 늘리기
        silence = AudioArrayClip(np.zeros((44100, 2)), fps=44100)
        silence = silence.set_duration(duration)
        silence.write_audiofile(audio_path, fps=44100, logger=None)

    # 이미지 클립 생성
    img_clip = ImageClip(image_path)
    
    # 오디오 클립 불러오기 및 길이 자르기
    audio_clip = AudioFileClip(audio_path)
    if audio_clip.duration > duration:
        audio_clip = audio_clip.subclip(0, duration)
        
    # 영상 길이를 40초로 고정하고 오디오 입히기
    video = img_clip.set_duration(duration)
    video = video.set_audio(audio_clip)
    
    # MP4 파일로 추출 (초당 1프레임으로 렌더링 속도 최적화)
    video.write_videofile(output_path, fps=1, codec="libx264", audio_codec="aac", logger=None)

import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 권한 범위 (유튜브 업로드용)
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    creds = None
    # token.pickle 파일에 사용자 로그인 정보가 저장되어 영구적으로 자동화가 가능해집니다.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # 유효한 자격 증명이 없으면 새로 로그인(최초 1회만 브라우저 열림)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secrets.json'):
                print("❌ ERROR: 유튜브 API 'client_secrets.json' 파일이 필요합니다!")
                print("구글 클라우드 콘솔에서 API 키를 발급받아 프로젝트 폴더에 넣어주세요.")
                exit(1)
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 갱신된(혹은 새로 발급받은) 자격 증명 저장
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, video_path, title, upload_date):
    # 날짜를 ISO 8601 형식으로 변환 (예약 시간에 필요)
    publish_at = upload_date.isoformat() + '.000Z' 

    body = {
        'snippet': {
            'title': title,
            'description': '2024년 최고의 재테크 꿀팁! #재테크 #투자 #자산관리',
            'tags': ['재테크', '금융', '투자'],
            'categoryId': '27' # 교육(27) 카테고리
        },
        'status': {
            'privacyStatus': 'private', # 예약 업로드를 위해 일단 비공개로 올림
            'publishAt': publish_at,    # 이 시간에 자동으로 공개 전환됨
            'selfDeclaredMadeForKids': False
        }
    }

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )

    response = insert_request.execute()
    print(f"🎬 업로드 성공! 영상 ID: {response['id']}")

<!DOCTYPE html>
<!-- saved from url=(0020)https://opadog.site/ -->
<html lang="ko" class="theme-dark" style="color-scheme: dark;"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><style data-emotion="cl-internal" data-s=""></style><link rel="preload" as="image" href="https://opadog.site/opadog-logo.png"><link rel="stylesheet" href="./오파독AI - AI 숏폼 콘텐츠 공장_files/c9314d0e787cb34f.css" data-precedence="next"><link rel="stylesheet" href="./오파독AI - AI 숏폼 콘텐츠 공장_files/54252f4f3e444f1a.css" data-precedence="next"><link rel="preload" as="script" fetchpriority="low" href="./오파독AI - AI 숏폼 콘텐츠 공장_files/0486fed93804e349.js.다운로드"><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/70d5e6639c535ab8.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/c9943865aaf158ce.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/5523b6080bb8fc13.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/1070d6c577be7186.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/2d249cb9bc10604b.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/8a9c4eb652aa2946.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/c4e773c6cc6699d1.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/turbopack-f0c8c34ca682cc26.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/40437a6df375aa7f.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/72d591b20bc7c2ed.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/6f797f2a41d8dd2f.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/a3551492d8356670.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/b59340e5e042fb68.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/47e9aa9c1683ddfb.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/4d0460a1bf79e696.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/05eb991dca8618c1.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/d8ad9666f67919ed.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/c93d17e2ac482b4c.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/ea89fd5704e3d7c3.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/d4a7f7b7002bce64.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/0ce1fb79df8d30f1.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/f0467d1e3fd7d5c3.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/3b8b9aef618266ac.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/clerk.browser.js.다운로드" data-clerk-js-script="true" async="" crossorigin="anonymous" data-clerk-publishable-key="pk_live_Y2xlcmsub3BhZG9nLnNpdGUk" data-clerk-proxy-url="https://opadog.site/__clerk"></script><link rel="preload" href="./오파독AI - AI 숏폼 콘텐츠 공장_files/js" as="script"><link rel="preload" href="https://opadog.site/__clerk/npm/@clerk/ui@1/dist/ui.browser.js" as="script" crossorigin="anonymous"><meta name="sentry-trace" content="a19e2f777d41a1378f97f8a680b46ee4-5d437ff9470662ee-0"><meta name="baggage" content="sentry-environment=vercel-production,sentry-release=4af2c393822e6395c91cbfca41711c5a989cb8fb,sentry-public_key=a785e7a23f1b02d28211b8c0f76da555,sentry-trace_id=a19e2f777d41a1378f97f8a680b46ee4,sentry-org_id=4511505976918016,sentry-sampled=false,sentry-sample_rand=0.23067035720788165,sentry-sample_rate=0.1"><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/a6dad97d9634a72d.js.다운로드" nomodule=""></script><link rel="preload" href="https://opadog.site/_next/static/media/5c285b27cdda1fe8-s.p.a62025f2.woff2" as="font" crossorigin="" type="font/woff2"><link rel="preload" href="https://opadog.site/_next/static/media/797e433ab948586e-s.p.29207c2f.woff2" as="font" crossorigin="" type="font/woff2"><style id="grabbit-visited-styles">
        .grabbit-visited,
        .grabbit-visited:link,
        .grabbit-visited:visited {
            color: #551A8B !important; /* Standard visited link purple */
        }
    </style><style type="text/css">[data-sonner-toaster][dir=ltr],html[dir=ltr]{--toast-icon-margin-start:-3px;--toast-icon-margin-end:4px;--toast-svg-margin-start:-1px;--toast-svg-margin-end:0px;--toast-button-margin-start:auto;--toast-button-margin-end:0;--toast-close-button-start:0;--toast-close-button-end:unset;--toast-close-button-transform:translate(-35%, -35%)}[data-sonner-toaster][dir=rtl],html[dir=rtl]{--toast-icon-margin-start:4px;--toast-icon-margin-end:-3px;--toast-svg-margin-start:0px;--toast-svg-margin-end:-1px;--toast-button-margin-start:0;--toast-button-margin-end:auto;--toast-close-button-start:unset;--toast-close-button-end:0;--toast-close-button-transform:translate(35%, -35%)}[data-sonner-toaster]{position:fixed;width:var(--width);font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;--gray1:hsl(0, 0%, 99%);--gray2:hsl(0, 0%, 97.3%);--gray3:hsl(0, 0%, 95.1%);--gray4:hsl(0, 0%, 93%);--gray5:hsl(0, 0%, 90.9%);--gray6:hsl(0, 0%, 88.7%);--gray7:hsl(0, 0%, 85.8%);--gray8:hsl(0, 0%, 78%);--gray9:hsl(0, 0%, 56.1%);--gray10:hsl(0, 0%, 52.3%);--gray11:hsl(0, 0%, 43.5%);--gray12:hsl(0, 0%, 9%);--border-radius:8px;box-sizing:border-box;padding:0;margin:0;list-style:none;outline:0;z-index:999999999;transition:transform .4s ease}@media (hover:none) and (pointer:coarse){[data-sonner-toaster][data-lifted=true]{transform:none}}[data-sonner-toaster][data-x-position=right]{right:var(--offset-right)}[data-sonner-toaster][data-x-position=left]{left:var(--offset-left)}[data-sonner-toaster][data-x-position=center]{left:50%;transform:translateX(-50%)}[data-sonner-toaster][data-y-position=top]{top:var(--offset-top)}[data-sonner-toaster][data-y-position=bottom]{bottom:var(--offset-bottom)}[data-sonner-toast]{--y:translateY(100%);--lift-amount:calc(var(--lift) * var(--gap));z-index:var(--z-index);position:absolute;opacity:0;transform:var(--y);touch-action:none;transition:transform .4s,opacity .4s,height .4s,box-shadow .2s;box-sizing:border-box;outline:0;overflow-wrap:anywhere}[data-sonner-toast][data-styled=true]{padding:16px;background:var(--normal-bg);border:1px solid var(--normal-border);color:var(--normal-text);border-radius:var(--border-radius);box-shadow:0 4px 12px rgba(0,0,0,.1);width:var(--width);font-size:13px;display:flex;align-items:center;gap:6px}[data-sonner-toast]:focus-visible{box-shadow:0 4px 12px rgba(0,0,0,.1),0 0 0 2px rgba(0,0,0,.2)}[data-sonner-toast][data-y-position=top]{top:0;--y:translateY(-100%);--lift:1;--lift-amount:calc(1 * var(--gap))}[data-sonner-toast][data-y-position=bottom]{bottom:0;--y:translateY(100%);--lift:-1;--lift-amount:calc(var(--lift) * var(--gap))}[data-sonner-toast][data-styled=true] [data-description]{font-weight:400;line-height:1.4;color:#3f3f3f}[data-rich-colors=true][data-sonner-toast][data-styled=true] [data-description]{color:inherit}[data-sonner-toaster][data-sonner-theme=dark] [data-description]{color:#e8e8e8}[data-sonner-toast][data-styled=true] [data-title]{font-weight:500;line-height:1.5;color:inherit}[data-sonner-toast][data-styled=true] [data-icon]{display:flex;height:16px;width:16px;position:relative;justify-content:flex-start;align-items:center;flex-shrink:0;margin-left:var(--toast-icon-margin-start);margin-right:var(--toast-icon-margin-end)}[data-sonner-toast][data-promise=true] [data-icon]>svg{opacity:0;transform:scale(.8);transform-origin:center;animation:sonner-fade-in .3s ease forwards}[data-sonner-toast][data-styled=true] [data-icon]>*{flex-shrink:0}[data-sonner-toast][data-styled=true] [data-icon] svg{margin-left:var(--toast-svg-margin-start);margin-right:var(--toast-svg-margin-end)}[data-sonner-toast][data-styled=true] [data-content]{display:flex;flex-direction:column;gap:2px}[data-sonner-toast][data-styled=true] [data-button]{border-radius:4px;padding-left:8px;padding-right:8px;height:24px;font-size:12px;color:var(--normal-bg);background:var(--normal-text);margin-left:var(--toast-button-margin-start);margin-right:var(--toast-button-margin-end);border:none;font-weight:500;cursor:pointer;outline:0;display:flex;align-items:center;flex-shrink:0;transition:opacity .4s,box-shadow .2s}[data-sonner-toast][data-styled=true] [data-button]:focus-visible{box-shadow:0 0 0 2px rgba(0,0,0,.4)}[data-sonner-toast][data-styled=true] [data-button]:first-of-type{margin-left:var(--toast-button-margin-start);margin-right:var(--toast-button-margin-end)}[data-sonner-toast][data-styled=true] [data-cancel]{color:var(--normal-text);background:rgba(0,0,0,.08)}[data-sonner-toaster][data-sonner-theme=dark] [data-sonner-toast][data-styled=true] [data-cancel]{background:rgba(255,255,255,.3)}[data-sonner-toast][data-styled=true] [data-close-button]{position:absolute;left:var(--toast-close-button-start);right:var(--toast-close-button-end);top:0;height:20px;width:20px;display:flex;justify-content:center;align-items:center;padding:0;color:var(--gray12);background:var(--normal-bg);border:1px solid var(--gray4);transform:var(--toast-close-button-transform);border-radius:50%;cursor:pointer;z-index:1;transition:opacity .1s,background .2s,border-color .2s}[data-sonner-toast][data-styled=true] [data-close-button]:focus-visible{box-shadow:0 4px 12px rgba(0,0,0,.1),0 0 0 2px rgba(0,0,0,.2)}[data-sonner-toast][data-styled=true] [data-disabled=true]{cursor:not-allowed}[data-sonner-toast][data-styled=true]:hover [data-close-button]:hover{background:var(--gray2);border-color:var(--gray5)}[data-sonner-toast][data-swiping=true]::before{content:'';position:absolute;left:-100%;right:-100%;height:100%;z-index:-1}[data-sonner-toast][data-y-position=top][data-swiping=true]::before{bottom:50%;transform:scaleY(3) translateY(50%)}[data-sonner-toast][data-y-position=bottom][data-swiping=true]::before{top:50%;transform:scaleY(3) translateY(-50%)}[data-sonner-toast][data-swiping=false][data-removed=true]::before{content:'';position:absolute;inset:0;transform:scaleY(2)}[data-sonner-toast][data-expanded=true]::after{content:'';position:absolute;left:0;height:calc(var(--gap) + 1px);bottom:100%;width:100%}[data-sonner-toast][data-mounted=true]{--y:translateY(0);opacity:1}[data-sonner-toast][data-expanded=false][data-front=false]{--scale:var(--toasts-before) * 0.05 + 1;--y:translateY(calc(var(--lift-amount) * var(--toasts-before))) scale(calc(-1 * var(--scale)));height:var(--front-toast-height)}[data-sonner-toast]>*{transition:opacity .4s}[data-sonner-toast][data-x-position=right]{right:0}[data-sonner-toast][data-x-position=left]{left:0}[data-sonner-toast][data-expanded=false][data-front=false][data-styled=true]>*{opacity:0}[data-sonner-toast][data-visible=false]{opacity:0;pointer-events:none}[data-sonner-toast][data-mounted=true][data-expanded=true]{--y:translateY(calc(var(--lift) * var(--offset)));height:var(--initial-height)}[data-sonner-toast][data-removed=true][data-front=true][data-swipe-out=false]{--y:translateY(calc(var(--lift) * -100%));opacity:0}[data-sonner-toast][data-removed=true][data-front=false][data-swipe-out=false][data-expanded=true]{--y:translateY(calc(var(--lift) * var(--offset) + var(--lift) * -100%));opacity:0}[data-sonner-toast][data-removed=true][data-front=false][data-swipe-out=false][data-expanded=false]{--y:translateY(40%);opacity:0;transition:transform .5s,opacity .2s}[data-sonner-toast][data-removed=true][data-front=false]::before{height:calc(var(--initial-height) + 20%)}[data-sonner-toast][data-swiping=true]{transform:var(--y) translateY(var(--swipe-amount-y,0)) translateX(var(--swipe-amount-x,0));transition:none}[data-sonner-toast][data-swiped=true]{user-select:none}[data-sonner-toast][data-swipe-out=true][data-y-position=bottom],[data-sonner-toast][data-swipe-out=true][data-y-position=top]{animation-duration:.2s;animation-timing-function:ease-out;animation-fill-mode:forwards}[data-sonner-toast][data-swipe-out=true][data-swipe-direction=left]{animation-name:swipe-out-left}[data-sonner-toast][data-swipe-out=true][data-swipe-direction=right]{animation-name:swipe-out-right}[data-sonner-toast][data-swipe-out=true][data-swipe-direction=up]{animation-name:swipe-out-up}[data-sonner-toast][data-swipe-out=true][data-swipe-direction=down]{animation-name:swipe-out-down}@keyframes swipe-out-left{from{transform:var(--y) translateX(var(--swipe-amount-x));opacity:1}to{transform:var(--y) translateX(calc(var(--swipe-amount-x) - 100%));opacity:0}}@keyframes swipe-out-right{from{transform:var(--y) translateX(var(--swipe-amount-x));opacity:1}to{transform:var(--y) translateX(calc(var(--swipe-amount-x) + 100%));opacity:0}}@keyframes swipe-out-up{from{transform:var(--y) translateY(var(--swipe-amount-y));opacity:1}to{transform:var(--y) translateY(calc(var(--swipe-amount-y) - 100%));opacity:0}}@keyframes swipe-out-down{from{transform:var(--y) translateY(var(--swipe-amount-y));opacity:1}to{transform:var(--y) translateY(calc(var(--swipe-amount-y) + 100%));opacity:0}}@media (max-width:600px){[data-sonner-toaster]{position:fixed;right:var(--mobile-offset-right);left:var(--mobile-offset-left);width:100%}[data-sonner-toaster][dir=rtl]{left:calc(var(--mobile-offset-left) * -1)}[data-sonner-toaster] [data-sonner-toast]{left:0;right:0;width:calc(100% - var(--mobile-offset-left) * 2)}[data-sonner-toaster][data-x-position=left]{left:var(--mobile-offset-left)}[data-sonner-toaster][data-y-position=bottom]{bottom:var(--mobile-offset-bottom)}[data-sonner-toaster][data-y-position=top]{top:var(--mobile-offset-top)}[data-sonner-toaster][data-x-position=center]{left:var(--mobile-offset-left);right:var(--mobile-offset-right);transform:none}}[data-sonner-toaster][data-sonner-theme=light]{--normal-bg:#fff;--normal-border:var(--gray4);--normal-text:var(--gray12);--success-bg:hsl(143, 85%, 96%);--success-border:hsl(145, 92%, 87%);--success-text:hsl(140, 100%, 27%);--info-bg:hsl(208, 100%, 97%);--info-border:hsl(221, 91%, 93%);--info-text:hsl(210, 92%, 45%);--warning-bg:hsl(49, 100%, 97%);--warning-border:hsl(49, 91%, 84%);--warning-text:hsl(31, 92%, 45%);--error-bg:hsl(359, 100%, 97%);--error-border:hsl(359, 100%, 94%);--error-text:hsl(360, 100%, 45%)}[data-sonner-toaster][data-sonner-theme=light] [data-sonner-toast][data-invert=true]{--normal-bg:#000;--normal-border:hsl(0, 0%, 20%);--normal-text:var(--gray1)}[data-sonner-toaster][data-sonner-theme=dark] [data-sonner-toast][data-invert=true]{--normal-bg:#fff;--normal-border:var(--gray3);--normal-text:var(--gray12)}[data-sonner-toaster][data-sonner-theme=dark]{--normal-bg:#000;--normal-bg-hover:hsl(0, 0%, 12%);--normal-border:hsl(0, 0%, 20%);--normal-border-hover:hsl(0, 0%, 25%);--normal-text:var(--gray1);--success-bg:hsl(150, 100%, 6%);--success-border:hsl(147, 100%, 12%);--success-text:hsl(150, 86%, 65%);--info-bg:hsl(215, 100%, 6%);--info-border:hsl(223, 43%, 17%);--info-text:hsl(216, 87%, 65%);--warning-bg:hsl(64, 100%, 6%);--warning-border:hsl(60, 100%, 9%);--warning-text:hsl(46, 87%, 65%);--error-bg:hsl(358, 76%, 10%);--error-border:hsl(357, 89%, 16%);--error-text:hsl(358, 100%, 81%)}[data-sonner-toaster][data-sonner-theme=dark] [data-sonner-toast] [data-close-button]{background:var(--normal-bg);border-color:var(--normal-border);color:var(--normal-text)}[data-sonner-toaster][data-sonner-theme=dark] [data-sonner-toast] [data-close-button]:hover{background:var(--normal-bg-hover);border-color:var(--normal-border-hover)}[data-rich-colors=true][data-sonner-toast][data-type=success]{background:var(--success-bg);border-color:var(--success-border);color:var(--success-text)}[data-rich-colors=true][data-sonner-toast][data-type=success] [data-close-button]{background:var(--success-bg);border-color:var(--success-border);color:var(--success-text)}[data-rich-colors=true][data-sonner-toast][data-type=info]{background:var(--info-bg);border-color:var(--info-border);color:var(--info-text)}[data-rich-colors=true][data-sonner-toast][data-type=info] [data-close-button]{background:var(--info-bg);border-color:var(--info-border);color:var(--info-text)}[data-rich-colors=true][data-sonner-toast][data-type=warning]{background:var(--warning-bg);border-color:var(--warning-border);color:var(--warning-text)}[data-rich-colors=true][data-sonner-toast][data-type=warning] [data-close-button]{background:var(--warning-bg);border-color:var(--warning-border);color:var(--warning-text)}[data-rich-colors=true][data-sonner-toast][data-type=error]{background:var(--error-bg);border-color:var(--error-border);color:var(--error-text)}[data-rich-colors=true][data-sonner-toast][data-type=error] [data-close-button]{background:var(--error-bg);border-color:var(--error-border);color:var(--error-text)}.sonner-loading-wrapper{--size:16px;height:var(--size);width:var(--size);position:absolute;inset:0;z-index:10}.sonner-loading-wrapper[data-visible=false]{transform-origin:center;animation:sonner-fade-out .2s ease forwards}.sonner-spinner{position:relative;top:50%;left:50%;height:var(--size);width:var(--size)}.sonner-loading-bar{animation:sonner-spin 1.2s linear infinite;background:var(--gray11);border-radius:6px;height:8%;left:-10%;position:absolute;top:-3.9%;width:24%}.sonner-loading-bar:first-child{animation-delay:-1.2s;transform:rotate(.0001deg) translate(146%)}.sonner-loading-bar:nth-child(2){animation-delay:-1.1s;transform:rotate(30deg) translate(146%)}.sonner-loading-bar:nth-child(3){animation-delay:-1s;transform:rotate(60deg) translate(146%)}.sonner-loading-bar:nth-child(4){animation-delay:-.9s;transform:rotate(90deg) translate(146%)}.sonner-loading-bar:nth-child(5){animation-delay:-.8s;transform:rotate(120deg) translate(146%)}.sonner-loading-bar:nth-child(6){animation-delay:-.7s;transform:rotate(150deg) translate(146%)}.sonner-loading-bar:nth-child(7){animation-delay:-.6s;transform:rotate(180deg) translate(146%)}.sonner-loading-bar:nth-child(8){animation-delay:-.5s;transform:rotate(210deg) translate(146%)}.sonner-loading-bar:nth-child(9){animation-delay:-.4s;transform:rotate(240deg) translate(146%)}.sonner-loading-bar:nth-child(10){animation-delay:-.3s;transform:rotate(270deg) translate(146%)}.sonner-loading-bar:nth-child(11){animation-delay:-.2s;transform:rotate(300deg) translate(146%)}.sonner-loading-bar:nth-child(12){animation-delay:-.1s;transform:rotate(330deg) translate(146%)}@keyframes sonner-fade-in{0%{opacity:0;transform:scale(.8)}100%{opacity:1;transform:scale(1)}}@keyframes sonner-fade-out{0%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(.8)}}@keyframes sonner-spin{0%{opacity:1}100%{opacity:.15}}@media (prefers-reduced-motion){.sonner-loading-bar,[data-sonner-toast],[data-sonner-toast]>*{transition:none!important;animation:none!important}}.sonner-loader{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);transform-origin:center;transition:opacity .2s,transform .2s}.sonner-loader[data-visible=false]{opacity:0;transform:scale(.8) translate(-50%,-50%)}</style><style type="text/css">@keyframes spin-668344b5{0%{transform:rotate(0deg)}to{transform:rotate(1turn)}}</style><style type="text/css">:root{--toastify-color-light:#fff;--toastify-color-dark:#121212;--toastify-color-info:#3498db;--toastify-color-success:#07bc0c;--toastify-color-warning:#f1c40f;--toastify-color-error:#e74c3c;--toastify-color-transparent:#ffffffb3;--toastify-icon-color-info:var(--toastify-color-info);--toastify-icon-color-success:var(--toastify-color-success);--toastify-icon-color-warning:var(--toastify-color-warning);--toastify-icon-color-error:var(--toastify-color-error);--toastify-toast-width:320px;--toastify-toast-background:#fff;--toastify-toast-min-height:64px;--toastify-toast-max-height:800px;--toastify-font-family:sans-serif;--toastify-z-index:9999;--toastify-text-color-light:#757575;--toastify-text-color-dark:#fff;--toastify-text-color-info:#fff;--toastify-text-color-success:#fff;--toastify-text-color-warning:#fff;--toastify-text-color-error:#fff;--toastify-spinner-color:#616161;--toastify-spinner-color-empty-area:#e0e0e0;--toastify-color-progress-light:linear-gradient(90deg,#4cd964,#5ac8fa,#007aff,#34aadc,#5856d6,#ff2d55);--toastify-color-progress-dark:#bb86fc;--toastify-color-progress-info:var(--toastify-color-info);--toastify-color-progress-success:var(--toastify-color-success);--toastify-color-progress-warning:var(--toastify-color-warning);--toastify-color-progress-error:var(--toastify-color-error);--toastify-color-progress-colored:#ddd}.Toastify__toast-container{box-sizing:border-box;color:#fff;padding:4px;position:fixed;transform:translate3d(0,0,var(--toastify-z-index) px);width:var(--toastify-toast-width);z-index:var(--toastify-z-index)}.Toastify__toast-container--top-left{left:1em;top:1em}.Toastify__toast-container--top-center{left:50%;top:1em;transform:translateX(-50%)}.Toastify__toast-container--top-right{right:1em;top:1em}.Toastify__toast-container--bottom-left{bottom:1em;left:1em}.Toastify__toast-container--bottom-center{bottom:1em;left:50%;transform:translateX(-50%)}.Toastify__toast-container--bottom-right{bottom:1em;right:1em}@media only screen and (max-width:480px){.Toastify__toast-container{left:0;margin:0;padding:0;width:100vw}.Toastify__toast-container--top-center,.Toastify__toast-container--top-left,.Toastify__toast-container--top-right{top:0;transform:translateX(0)}.Toastify__toast-container--bottom-center,.Toastify__toast-container--bottom-left,.Toastify__toast-container--bottom-right{bottom:0;transform:translateX(0)}.Toastify__toast-container--rtl{left:auto;right:0}}.Toastify__toast{border-radius:4px;box-shadow:0 1px 10px 0 #0000001a,0 2px 15px 0 #0000000d;box-sizing:border-box;cursor:pointer;direction:ltr;display:flex;font-family:var(--toastify-font-family);justify-content:space-between;margin-bottom:1rem;max-height:var(--toastify-toast-max-height);min-height:var(--toastify-toast-min-height);overflow:hidden;padding:8px;position:relative;z-index:0}.Toastify__toast--rtl{direction:rtl}.Toastify__toast-body{align-items:center;display:flex;flex:1 1 auto;margin:auto 0;padding:6px;white-space:pre-wrap}.Toastify__toast-body>div:last-child{flex:1}.Toastify__toast-icon{display:flex;flex-shrink:0;margin-inline-end:10px;width:20px}.Toastify--animate{animation-duration:.7s;animation-fill-mode:both}.Toastify--animate-icon{animation-duration:.3s;animation-fill-mode:both}@media only screen and (max-width:480px){.Toastify__toast{border-radius:0;margin-bottom:0}}.Toastify__toast-theme--dark{background:var(--toastify-color-dark);color:var(--toastify-text-color-dark)}.Toastify__toast-theme--colored.Toastify__toast--default,.Toastify__toast-theme--light{background:var(--toastify-color-light);color:var(--toastify-text-color-light)}.Toastify__toast-theme--colored.Toastify__toast--info{background:var(--toastify-color-info);color:var(--toastify-text-color-info)}.Toastify__toast-theme--colored.Toastify__toast--success{background:var(--toastify-color-success);color:var(--toastify-text-color-success)}.Toastify__toast-theme--colored.Toastify__toast--warning{background:var(--toastify-color-warning);color:var(--toastify-text-color-warning)}.Toastify__toast-theme--colored.Toastify__toast--error{background:var(--toastify-color-error);color:var(--toastify-text-color-error)}.Toastify__progress-bar-theme--light{background:var(--toastify-color-progress-light)}.Toastify__progress-bar-theme--dark{background:var(--toastify-color-progress-dark)}.Toastify__progress-bar--info{background:var(--toastify-color-progress-info)}.Toastify__progress-bar--success{background:var(--toastify-color-progress-success)}.Toastify__progress-bar--warning{background:var(--toastify-color-progress-warning)}.Toastify__progress-bar--error{background:var(--toastify-color-progress-error)}.Toastify__progress-bar-theme--colored.Toastify__progress-bar--default{background:var(--toastify-color-progress-colored)}.Toastify__progress-bar-theme--colored.Toastify__progress-bar--error,.Toastify__progress-bar-theme--colored.Toastify__progress-bar--info,.Toastify__progress-bar-theme--colored.Toastify__progress-bar--success,.Toastify__progress-bar-theme--colored.Toastify__progress-bar--warning{background:var(--toastify-color-transparent)}.Toastify__close-button{align-self:flex-start;background:#0000;border:none;color:#fff;cursor:pointer;opacity:.7;outline:none;padding:0;transition:.3s ease}.Toastify__close-button--light{color:#000;opacity:.3}.Toastify__close-button>svg{fill:currentcolor;height:16px;width:14px}.Toastify__close-button:focus,.Toastify__close-button:hover{opacity:1}@keyframes Toastify__trackProgress{0%{transform:scaleX(1)}to{transform:scaleX(0)}}.Toastify__progress-bar{bottom:0;height:5px;left:0;opacity:.7;position:absolute;transform-origin:left;width:100%;z-index:var(--toastify-z-index)}.Toastify__progress-bar--animated{animation:Toastify__trackProgress linear 1 forwards}.Toastify__progress-bar--controlled{transition:transform .2s}.Toastify__progress-bar--rtl{left:auto;right:0;transform-origin:right}.Toastify__spinner{animation:Toastify__spin .65s linear infinite;border:2px solid;border-color:var(--toastify-spinner-color-empty-area);border-radius:100%;border-right-color:var(--toastify-spinner-color);box-sizing:border-box;height:20px;width:20px}@keyframes Toastify__bounceInRight{0%,60%,75%,90%,to{animation-timing-function:cubic-bezier(.215,.61,.355,1)}0%{opacity:0;transform:translate3d(3000px,0,0)}60%{opacity:1;transform:translate3d(-25px,0,0)}75%{transform:translate3d(10px,0,0)}90%{transform:translate3d(-5px,0,0)}to{transform:none}}@keyframes Toastify__bounceOutRight{20%{opacity:1;transform:translate3d(-20px,0,0)}to{opacity:0;transform:translate3d(2000px,0,0)}}@keyframes Toastify__bounceInLeft{0%,60%,75%,90%,to{animation-timing-function:cubic-bezier(.215,.61,.355,1)}0%{opacity:0;transform:translate3d(-3000px,0,0)}60%{opacity:1;transform:translate3d(25px,0,0)}75%{transform:translate3d(-10px,0,0)}90%{transform:translate3d(5px,0,0)}to{transform:none}}@keyframes Toastify__bounceOutLeft{20%{opacity:1;transform:translate3d(20px,0,0)}to{opacity:0;transform:translate3d(-2000px,0,0)}}@keyframes Toastify__bounceInUp{0%,60%,75%,90%,to{animation-timing-function:cubic-bezier(.215,.61,.355,1)}0%{opacity:0;transform:translate3d(0,3000px,0)}60%{opacity:1;transform:translate3d(0,-20px,0)}75%{transform:translate3d(0,10px,0)}90%{transform:translate3d(0,-5px,0)}to{transform:translateZ(0)}}@keyframes Toastify__bounceOutUp{20%{transform:translate3d(0,-10px,0)}40%,45%{opacity:1;transform:translate3d(0,20px,0)}to{opacity:0;transform:translate3d(0,-2000px,0)}}@keyframes Toastify__bounceInDown{0%,60%,75%,90%,to{animation-timing-function:cubic-bezier(.215,.61,.355,1)}0%{opacity:0;transform:translate3d(0,-3000px,0)}60%{opacity:1;transform:translate3d(0,25px,0)}75%{transform:translate3d(0,-10px,0)}90%{transform:translate3d(0,5px,0)}to{transform:none}}@keyframes Toastify__bounceOutDown{20%{transform:translate3d(0,10px,0)}40%,45%{opacity:1;transform:translate3d(0,-20px,0)}to{opacity:0;transform:translate3d(0,2000px,0)}}.Toastify__bounce-enter--bottom-left,.Toastify__bounce-enter--top-left{animation-name:Toastify__bounceInLeft}.Toastify__bounce-enter--bottom-right,.Toastify__bounce-enter--top-right{animation-name:Toastify__bounceInRight}.Toastify__bounce-enter--top-center{animation-name:Toastify__bounceInDown}.Toastify__bounce-enter--bottom-center{animation-name:Toastify__bounceInUp}.Toastify__bounce-exit--bottom-left,.Toastify__bounce-exit--top-left{animation-name:Toastify__bounceOutLeft}.Toastify__bounce-exit--bottom-right,.Toastify__bounce-exit--top-right{animation-name:Toastify__bounceOutRight}.Toastify__bounce-exit--top-center{animation-name:Toastify__bounceOutUp}.Toastify__bounce-exit--bottom-center{animation-name:Toastify__bounceOutDown}@keyframes Toastify__none{0%,60%,75%,90%,to{animation-duration:0;animation-timing-function:none}0%{opacity:1;transform:translateZ(0)}to{transform:translateZ(0)}}.Toastify__none-enter--bottom-center,.Toastify__none-enter--bottom-left,.Toastify__none-enter--bottom-right,.Toastify__none-enter--top-center,.Toastify__none-enter--top-left,.Toastify__none-enter--top-right{animation-name:Toastify__none}@keyframes Toastify__zoomIn{0%{opacity:0;transform:scale3d(.3,.3,.3)}50%{opacity:1}}@keyframes Toastify__zoomOut{0%{opacity:1}50%{opacity:0;transform:scale3d(.3,.3,.3)}to{opacity:0}}.Toastify__zoom-enter{animation-name:Toastify__zoomIn}.Toastify__zoom-exit{animation-name:Toastify__zoomOut}@keyframes Toastify__flipIn{0%{animation-timing-function:ease-in;opacity:0;transform:perspective(400px) rotateX(90deg)}40%{animation-timing-function:ease-in;transform:perspective(400px) rotateX(-20deg)}60%{opacity:1;transform:perspective(400px) rotateX(10deg)}80%{transform:perspective(400px) rotateX(-5deg)}to{transform:perspective(400px)}}@keyframes Toastify__flipOut{0%{transform:perspective(400px)}30%{opacity:1;transform:perspective(400px) rotateX(-20deg)}to{opacity:0;transform:perspective(400px) rotateX(90deg)}}.Toastify__flip-enter{animation-name:Toastify__flipIn}.Toastify__flip-exit{animation-name:Toastify__flipOut}@keyframes Toastify__slideInRight{0%{transform:translate3d(110%,0,0);visibility:visible}to{transform:translateZ(0)}}@keyframes Toastify__slideInLeft{0%{transform:translate3d(-110%,0,0);visibility:visible}to{transform:translateZ(0)}}@keyframes Toastify__slideInUp{0%{transform:translate3d(0,110%,0);visibility:visible}to{transform:translateZ(0)}}@keyframes Toastify__slideInDown{0%{transform:translate3d(0,-110%,0);visibility:visible}to{transform:translateZ(0)}}@keyframes Toastify__slideOutRight{0%{transform:translateZ(0)}to{transform:translate3d(110%,0,0);visibility:hidden}}@keyframes Toastify__slideOutLeft{0%{transform:translateZ(0)}to{transform:translate3d(-110%,0,0);visibility:hidden}}@keyframes Toastify__slideOutDown{0%{transform:translateZ(0)}to{transform:translate3d(0,500px,0);visibility:hidden}}@keyframes Toastify__slideOutUp{0%{transform:translateZ(0)}to{transform:translate3d(0,-500px,0);visibility:hidden}}.Toastify__slide-enter--bottom-left,.Toastify__slide-enter--top-left{animation-name:Toastify__slideInLeft}.Toastify__slide-enter--bottom-right,.Toastify__slide-enter--top-right{animation-name:Toastify__slideInRight}.Toastify__slide-enter--top-center{animation-name:Toastify__slideInDown}.Toastify__slide-enter--bottom-center{animation-name:Toastify__slideInUp}.Toastify__slide-exit--bottom-left,.Toastify__slide-exit--top-left{animation-name:Toastify__slideOutLeft}.Toastify__slide-exit--bottom-right,.Toastify__slide-exit--top-right{animation-name:Toastify__slideOutRight}.Toastify__slide-exit--top-center{animation-name:Toastify__slideOutUp}.Toastify__slide-exit--bottom-center{animation-name:Toastify__slideOutDown}@keyframes Toastify__spin{0%{transform:rotate(0deg)}to{transform:rotate(1turn)}}</style><style id="qr-scanner-styles">
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        </style><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/6269b19bc13b4d40.js.다운로드"></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/c2d9b5524bff6cfc.js.다운로드"></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/45f6106264ccc4b9.js.다운로드"></script><meta name="viewport" content="width=device-width, initial-scale=1"><title>오파독AI - AI 숏폼 콘텐츠 공장</title><meta name="description" content="콘텐츠 기획부터 제작까지, AI가 대신합니다. 80+ 전문 스킬로 멀티 플랫폼 콘텐츠를 몇 분 만에 완성하세요."><link rel="icon" href="https://opadog.site/favicon.ico?favicon.0b3bf435.ico" sizes="256x256" type="image/x-icon"><link rel="icon" href="https://opadog.site/icon.png"><meta name="next-size-adjust" content=""><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/6269b19bc13b4d40.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/c2d9b5524bff6cfc.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/45f6106264ccc4b9.js.다운로드" async=""></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/46aad3999c1c0d04.js.다운로드"></script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/ab07b8c3700e6876.js.다운로드"></script></head><body class="dm_sans_45853038-module__6lgKKq__variable geist_mono_8d43a2aa-module__8Li5zG__variable antialiased"><!--$--><!--/$--><div hidden=""></div><script>((e,t,r,i,s,n,a,o)=>{let u=document.documentElement,l=["light","dark"];function c(t){var r;(Array.isArray(e)?e:[e]).forEach(e=>{let r="class"===e,i=r&&n?s.map(e=>n[e]||e):s;r?(u.classList.remove(...i),u.classList.add(n&&n[t]?n[t]:t)):u.setAttribute(e,t)}),r=t,o&&l.includes(r)&&(u.style.colorScheme=r)}if(i)c(i);else try{let e=localStorage.getItem(t)||r,i=a&&"system"===e?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":e;c(i)}catch(e){}})("class","theme","dark",null,["light","dark"],{"light":"light","dark":"theme-dark"},false,true)</script><div class="landing-surface min-h-screen"><nav class="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background/80 backdrop-blur-xl"><div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-6"><a class="text-xl font-bold" href="https://opadog.site/welcome"><span class="text-primary">오파독AI</span></a><div class="hidden items-center gap-8 md:flex"><a href="https://opadog.site/welcome#solution" class="text-sm text-foreground-subtle transition-colors hover:text-foreground">기능</a><a class="text-sm text-foreground-subtle transition-colors hover:text-foreground" href="https://opadog.site/tools">무료 도구</a><a href="https://opadog.site/welcome#pricing" class="text-sm text-foreground-subtle transition-colors hover:text-foreground">가격</a><a href="https://opadog.site/welcome#faq" class="text-sm text-foreground-subtle transition-colors hover:text-foreground">FAQ</a><button class="text-sm text-secondary-foreground transition-colors hover:text-foreground">로그인</button><button class="rounded-lg bg-primary px-5 py-2 text-sm font-medium text-primary-foreground transition-transform hover:scale-105">무료로 시작하기</button></div><button class="text-foreground-subtle md:hidden" aria-label="Toggle menu"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu h-6 w-6" aria-hidden="true"><path d="M4 5h16"></path><path d="M4 12h16"></path><path d="M4 19h16"></path></svg></button></div></nav><main><section class="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 pt-16"><div class="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"><div class="h-[600px] w-[600px] rounded-full bg-primary/10 blur-[120px]"></div></div><div class="pointer-events-none absolute top-1/3 right-1/4"><div class="h-[300px] w-[300px] rounded-full bg-chart-2/10 blur-[100px]"></div></div><div class="relative z-10 flex max-w-4xl flex-col items-center text-center"><div class="mb-8 inline-flex items-center rounded-full border border-border-strong bg-background/80 px-4 py-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles mr-2 h-4 w-4 text-primary" aria-hidden="true"><path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"></path><path d="M20 2v4"></path><path d="M22 4h-4"></path><circle cx="4" cy="20" r="2"></circle></svg>AI 숏폼 콘텐츠에 최적화된 올인원 툴</div><h1 class="mb-6 text-5xl font-extrabold leading-tight tracking-tight md:text-7xl"><span class="text-foreground">콘텐츠 기획부터 제작까지</span><br><span class="text-primary">AI가 대신합니다</span></h1><p class="mb-10 max-w-xl text-lg text-foreground-subtle md:text-xl">80+ 전문 AI 스킬로 멀티 플랫폼 숏폼 콘텐츠를 몇 분 만에 완성하세요.<br class="hidden md:block">기획, 대본, 제작, 발행까지 한 곳에서.</p><div class="mb-6 flex flex-col items-center gap-3 sm:flex-row"><button class="rounded-xl bg-primary px-10 py-4 text-lg font-semibold text-primary-foreground shadow-lg shadow-primary/25 transition-transform hover:scale-105">무료로 시작하기</button><a href="https://opadog.site/#solution" class="rounded-xl border border-border-strong bg-surface-2 px-8 py-4 text-lg font-medium text-secondary-foreground transition-colors hover:bg-surface-3">자세히 보기</a></div><div class="flex items-center gap-4 text-sm text-muted-foreground"><span class="flex items-center gap-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-zap h-3.5 w-3.5 text-primary" aria-hidden="true"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path></svg>가입 즉시 100 크레딧 무료</span><span class="text-foreground-faint">|</span><span>카드 등록 불필요</span></div><div class="mt-16 grid w-full max-w-3xl grid-cols-1 gap-4 sm:grid-cols-3"><div class="rounded-xl border border-border bg-card p-5 text-left"><div class="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles h-5 w-5 text-primary" aria-hidden="true"><path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"></path><path d="M20 2v4"></path><path d="M22 4h-4"></path><circle cx="4" cy="20" r="2"></circle></svg></div><h3 class="mb-1 text-sm font-semibold text-foreground">멀티모델 AI 채팅</h3><p class="text-xs text-muted-foreground">Gemini, Claude 등 여러 AI를 한 곳에서 활용</p></div><div class="rounded-xl border border-border bg-card p-5 text-left"><div class="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-chart-2/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-zap h-5 w-5 text-chart-2" aria-hidden="true"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path></svg></div><h3 class="mb-1 text-sm font-semibold text-foreground">80+ 전문 스킬</h3><p class="text-xs text-muted-foreground">플랫폼별로 최적화된 콘텐츠를 자동 생성</p></div><div class="rounded-xl border border-border bg-card p-5 text-left"><div class="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-ai/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-globe h-5 w-5 text-violet-400" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg></div><h3 class="mb-1 text-sm font-semibold text-foreground">원클릭 멀티채널 발행</h3><p class="text-xs text-muted-foreground">Instagram, YouTube, TikTok 등 한 번에 업로드</p></div></div></div></section><section class="relative py-24 px-6"><div class="mx-auto flex max-w-4xl flex-col items-center text-center"><div class="mb-4 text-8xl font-black tracking-tight text-foreground md:text-[120px]" style="text-shadow: rgba(16, 185, 129, 0.5) 0px 0px 80px, rgba(6, 182, 212, 0.3) 0px 0px 30px;">0x</div><p class="mb-16 text-xl text-foreground-subtle">콘텐츠 생산성 향상</p><div class="grid w-full max-w-2xl grid-cols-3 gap-8"><div class="flex flex-col items-center"><span class="text-2xl font-bold text-foreground md:text-3xl">5분</span><span class="mt-1 text-sm text-muted-foreground">콘텐츠 1개 생성 시간</span></div><div class="flex flex-col items-center"><span class="text-2xl font-bold text-foreground md:text-3xl">5채널+</span><span class="mt-1 text-sm text-muted-foreground">동시 업로드 지원</span></div><div class="flex flex-col items-center"><span class="text-2xl font-bold text-foreground md:text-3xl">24/7</span><span class="mt-1 text-sm text-muted-foreground">자동 예약 발행</span></div></div></div></section><section class="relative py-24 px-6"><div class="mx-auto max-w-4xl"><h2 class="mb-14 text-center text-3xl font-bold text-foreground md:text-4xl">이런 고민, 있으시죠?</h2><div class="grid gap-5 md:grid-cols-2"><div class="group rounded-xl border border-destructive/20 bg-card p-6 transition-all hover:border-destructive/40 hover:shadow-[0_0_30px_rgba(239,68,68,0.05)]"><span class="mb-3 block text-2xl">⏰</span><p class="text-lg text-secondary-foreground">콘텐츠 기획에 매번 몇 시간씩...</p></div><div class="group rounded-xl border border-destructive/20 bg-card p-6 transition-all hover:border-destructive/40 hover:shadow-[0_0_30px_rgba(239,68,68,0.05)]"><span class="mb-3 block text-2xl">🎬</span><p class="text-lg text-secondary-foreground">영상 편집은 더 오래 걸리고...</p></div><div class="group rounded-xl border border-destructive/20 bg-card p-6 transition-all hover:border-destructive/40 hover:shadow-[0_0_30px_rgba(239,68,68,0.05)]"><span class="mb-3 block text-2xl">📱</span><p class="text-lg text-secondary-foreground">각 채널마다 따로 업로드하는 번거로움</p></div><div class="group rounded-xl border border-destructive/20 bg-card p-6 transition-all hover:border-destructive/40 hover:shadow-[0_0_30px_rgba(239,68,68,0.05)]"><span class="mb-3 block text-2xl">🤖</span><p class="text-lg text-secondary-foreground">자동화? 어디서부터 시작해야 할지...</p></div></div><p class="mt-12 text-center text-3xl font-bold"><span class="text-destructive">악순환</span></p></div></section><section id="solution" class="relative py-24 px-6"><div class="mx-auto max-w-2xl"><h2 class="mb-16 text-center text-3xl font-bold text-foreground md:text-4xl">딱 <span class="text-primary">3단계</span>면 됩니다</h2><div class="flex flex-col items-center gap-0"><div class="flex w-full max-w-sm flex-col items-center"><div class="relative w-full overflow-hidden rounded-xl bg-card px-8 py-6"><div class="pointer-events-none absolute inset-0 rounded-xl border-2 border-transparent bg-gradient-to-b from-primary/70 to-primary/20 [mask:linear-gradient(#fff_0_0)_content-box,linear-gradient(#fff_0_0)] [mask-composite:xor] p-[2px]" style="mask-composite: xor;"></div><div class="relative z-10"><p class="mb-1 text-sm font-medium text-primary">1단계</p><h3 class="mb-2 text-xl font-bold text-foreground">AI 기획 자동화</h3><p class="text-sm text-foreground-subtle">주제만 입력하면 AI가 트렌드를 분석하여 콘텐츠 아이디어를 자동 생성합니다</p></div></div><div class="flex h-12 items-center justify-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down h-6 w-6 animate-bounce text-primary" aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg></div></div><div class="flex w-full max-w-sm flex-col items-center"><div class="relative w-full overflow-hidden rounded-xl bg-card px-8 py-6"><div class="pointer-events-none absolute inset-0 rounded-xl border-2 border-transparent bg-gradient-to-b from-primary/70 to-primary/20 [mask:linear-gradient(#fff_0_0)_content-box,linear-gradient(#fff_0_0)] [mask-composite:xor] p-[2px]" style="mask-composite: xor;"></div><div class="relative z-10"><p class="mb-1 text-sm font-medium text-primary">2단계</p><h3 class="mb-2 text-xl font-bold text-foreground">AI 콘텐츠 제작</h3><p class="text-sm text-foreground-subtle">카드뉴스, 블로그, SNS 게시물을 AI가 자동으로 디자인하고 작성합니다</p></div></div><div class="flex h-12 items-center justify-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down h-6 w-6 animate-bounce text-primary" aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg></div></div><div class="flex w-full max-w-sm flex-col items-center"><div class="relative w-full overflow-hidden rounded-xl bg-card px-8 py-6"><div class="pointer-events-none absolute inset-0 rounded-xl border-2 border-transparent bg-gradient-to-b from-primary to-primary/30 [mask:linear-gradient(#fff_0_0)_content-box,linear-gradient(#fff_0_0)] [mask-composite:xor] p-[2px]" style="mask-composite: xor;"></div><div class="relative z-10"><p class="mb-1 text-sm font-medium text-primary">3단계</p><h3 class="mb-2 text-xl font-bold text-foreground">멀티채널 자동 배포</h3><p class="text-sm text-foreground-subtle">인스타, 스레드, X, 링크드인, 유튜브까지 한 번에 예약 발행합니다</p></div></div></div></div></div></section><section id="benefits" class="relative py-24 px-6"><div class="mx-auto max-w-5xl"><h2 class="mb-14 text-center text-3xl font-bold text-foreground md:text-4xl">왜 <span class="text-primary">오파독AI</span>인가요?</h2><div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-5"><div class="group rounded-xl border border-border bg-card p-6 text-center transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]"><span class="mb-4 block text-3xl">⚡</span><h3 class="mb-2 text-lg font-semibold text-foreground">시간 단축</h3><p class="text-sm text-foreground-subtle">기획~업로드 1/10 시간</p></div><div class="group rounded-xl border border-border bg-card p-6 text-center transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]"><span class="mb-4 block text-3xl">💰</span><h3 class="mb-2 text-lg font-semibold text-foreground">저비용</h3><p class="text-sm text-foreground-subtle">월 5만원 이하로 운영</p></div><div class="group rounded-xl border border-border bg-card p-6 text-center transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]"><span class="mb-4 block text-3xl">📈</span><h3 class="mb-2 text-lg font-semibold text-foreground">멀티채널</h3><p class="text-sm text-foreground-subtle">5개 플랫폼 동시 발행</p></div><div class="group rounded-xl border border-border bg-card p-6 text-center transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]"><span class="mb-4 block text-3xl">🎓</span><h3 class="mb-2 text-lg font-semibold text-foreground">쉬운 사용</h3><p class="text-sm text-foreground-subtle">버튼 클릭만으로 완성</p></div><div class="group rounded-xl border border-border bg-card p-6 text-center transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]"><span class="mb-4 block text-3xl">📊</span><h3 class="mb-2 text-lg font-semibold text-foreground">수익 다변화</h3><p class="text-sm text-foreground-subtle">여러 채널에서 수익 창출</p></div></div></div></section><section id="tools" class="relative py-24 px-6"><div class="mx-auto max-w-5xl"><p class="mb-4 text-center text-sm font-medium tracking-wider text-primary uppercase">Free Tools</p><h2 class="mb-4 text-center text-3xl font-bold text-foreground md:text-4xl"><span class="text-primary">무료 마케팅 도구</span></h2><p class="mb-14 text-center text-foreground-subtle">로그인 없이 바로 사용할 수 있는 26가지 실용 도구</p><div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3"><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/character-counter"><span class="absolute top-4 right-4 rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-medium text-primary">인기</span><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-type size-5 text-primary" aria-hidden="true"><path d="M12 4v16"></path><path d="M4 7V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2"></path><path d="M9 20h6"></path></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">SNS 글자수 카운터</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">플랫폼별 글자수 제한을 실시간으로 확인하세요</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/vat-calculator"><span class="absolute top-4 right-4 rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-medium text-primary">인기</span><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-receipt size-5 text-primary" aria-hidden="true"><path d="M12 17V7"></path><path d="M16 8h-6a2 2 0 0 0 0 4h4a2 2 0 0 1 0 4H8"></path><path d="M4 3a1 1 0 0 1 1-1 1.3 1.3 0 0 1 .7.2l.933.6a1.3 1.3 0 0 0 1.4 0l.934-.6a1.3 1.3 0 0 1 1.4 0l.933.6a1.3 1.3 0 0 0 1.4 0l.933-.6a1.3 1.3 0 0 1 1.4 0l.934.6a1.3 1.3 0 0 0 1.4 0l.933-.6A1.3 1.3 0 0 1 19 2a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1 1.3 1.3 0 0 1-.7-.2l-.933-.6a1.3 1.3 0 0 0-1.4 0l-.934.6a1.3 1.3 0 0 1-1.4 0l-.933-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-1.4 0l-.934-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-.7.2 1 1 0 0 1-1-1z"></path></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">부가세 계산기</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">합계 금액 또는 공급가액에서 부가세를 즉시 계산합니다</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/salary-calculator"><span class="absolute top-4 right-4 rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-medium text-primary">인기</span><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-banknote size-5 text-primary" aria-hidden="true"><rect width="20" height="12" x="2" y="6" rx="2"></rect><circle cx="12" cy="12" r="2"></circle><path d="M6 12h.01M18 12h.01"></path></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">연봉 실수령액 계산기</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">연봉에서 4대보험, 소득세를 공제한 실수령액을 계산합니다</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/hashtag-generator"><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-hash size-5 text-primary" aria-hidden="true"><line x1="4" x2="20" y1="9" y2="9"></line><line x1="4" x2="20" y1="15" y2="15"></line><line x1="10" x2="8" y1="3" y2="21"></line><line x1="16" x2="14" y1="3" y2="21"></line></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">해시태그 생성기</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">키워드를 입력하면 인기 해시태그를 추천해드립니다</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/image-compressor"><span class="absolute top-4 right-4 rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-medium text-primary">NEW</span><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-image-down size-5 text-primary" aria-hidden="true"><path d="M10.3 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10l-3.1-3.1a2 2 0 0 0-2.814.014L6 21"></path><path d="m14 19 3 3v-5.5"></path><path d="m17 22 3-3"></path><circle cx="9" cy="9" r="2"></circle></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">이미지 압축기</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">브라우저에서 직접 이미지를 압축하는 무료 도구입니다</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/image-prompt-generator"><span class="absolute top-4 right-4 rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-medium text-primary">NEW</span><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-image-plus size-5 text-primary" aria-hidden="true"><path d="M16 5h6"></path><path d="M19 2v6"></path><path d="M21 11.5V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7.5"></path><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path><circle cx="9" cy="9" r="2"></circle></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">이미지 프롬프트 생성기</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">Midjourney, DALL-E, Stable Diffusion용 프롬프트를 생성합니다</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/marketing-calculator"><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calculator size-5 text-primary" aria-hidden="true"><rect width="16" height="20" x="4" y="2" rx="2"></rect><line x1="8" x2="16" y1="6" y2="6"></line><line x1="16" x2="16" y1="14" y2="18"></line><path d="M16 10h.01"></path><path d="M12 10h.01"></path><path d="M8 10h.01"></path><path d="M12 14h.01"></path><path d="M8 14h.01"></path><path d="M12 18h.01"></path><path d="M8 18h.01"></path></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">ROAS / 마케팅 계산기</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">광고비, 매출, 노출수로 ROAS, CPC, CTR을 즉시 계산</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/pdf-tools"><span class="absolute top-4 right-4 rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-medium text-primary">NEW</span><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-text size-5 text-primary" aria-hidden="true"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"></path><path d="M14 2v5a1 1 0 0 0 1 1h5"></path><path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">PDF 병합/분할 도구</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">브라우저에서 직접 PDF를 병합하고 분할합니다</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a><a class="group relative rounded-xl border border-border bg-card p-6 transition-all hover:border-border-strong hover:shadow-[0_0_30px_rgba(16,185,129,0.05)]" href="https://opadog.site/tools/spelling-checker"><span class="absolute top-4 right-4 rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-medium text-primary">NEW</span><div class="mb-4 flex size-11 items-center justify-center rounded-lg bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-spell-check size-5 text-primary" aria-hidden="true"><path d="m6 16 6-12 6 12"></path><path d="M8 12h8"></path><path d="m16 20 2 2 4-4"></path></svg></div><h3 class="mb-2 text-lg font-semibold text-foreground">맞춤법 수정기</h3><p class="mb-4 text-sm text-foreground-subtle leading-relaxed">한국어 맞춤법과 띄어쓰기를 자동으로 교정합니다</p><span class="inline-flex items-center gap-1 text-sm text-primary group-hover:gap-2 transition-all">사용하기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span></a></div><div class="mt-10 text-center"><a class="inline-flex items-center gap-2 rounded-lg border border-border-strong bg-surface-3 px-6 py-3 text-sm font-medium text-foreground transition-all hover:border-border-strong hover:bg-accent" href="https://opadog.site/tools">전체 26개 도구 보기 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right size-3.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></a></div></div></section><section id="pricing" class="relative py-24 px-6"><div class="mx-auto max-w-6xl"><h2 class="mb-4 text-center text-3xl font-bold text-foreground md:text-4xl"><span class="text-primary">합리적인 가격</span>으로 시작하세요</h2><p class="mb-16 text-center text-foreground-subtle">무료로 시작하고, 비즈니스에 맞게 업그레이드하세요</p><div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4"><div class="relative flex flex-col rounded-2xl border p-6 transition-all hover:scale-[1.02] border-border bg-card"><div class="mb-6"><h3 class="mb-1 text-lg font-bold text-foreground">무료</h3><p class="text-xs text-muted-foreground"></p></div><div class="mb-6"><span class="text-3xl font-black text-foreground">₩0</span></div><ul class="mb-8 flex-1 space-y-3"><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>AI 크레딧 100/월</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>기본 AI 채팅 (Gemini Flash)</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>템플릿 5개</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>라이브러리 저장 (50개)</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>콘텐츠 캘린더</li></ul><a class="block rounded-lg py-2.5 text-center text-sm font-medium transition-all border border-border-strong text-secondary-foreground hover:bg-accent" href="https://opadog.site/upgrade">시작하기</a></div><div class="relative flex flex-col rounded-2xl border p-6 transition-all hover:scale-[1.02] border-primary/50 bg-gradient-to-b from-primary/10 to-transparent shadow-lg shadow-primary/10"><div class="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-primary px-3 py-0.5 text-xs font-bold text-primary-foreground">추천</div><div class="mb-6"><h3 class="mb-1 text-lg font-bold text-foreground">플러스</h3><p class="text-xs text-muted-foreground">본격적인 콘텐츠 마케팅 시작</p></div><div class="mb-6"><span class="text-3xl font-black text-foreground">₩49,000</span><span class="text-sm text-muted-foreground">/월</span></div><ul class="mb-8 flex-1 space-y-3"><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>AI 크레딧 1,400/월</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>전체 AI 모델 (Gemini Pro, Claude)</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>전체 템플릿</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>SNS 인사이트</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>브랜드 보이스 3개</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>SNS 자동 배포 (2채널)</li></ul><a class="block rounded-lg py-2.5 text-center text-sm font-medium transition-all bg-primary text-primary-foreground hover:bg-primary-hover" href="https://opadog.site/upgrade">시작하기</a></div><div class="relative flex flex-col rounded-2xl border p-6 transition-all hover:scale-[1.02] border-border bg-card"><div class="mb-6"><h3 class="mb-1 text-lg font-bold text-foreground">프로</h3><p class="text-xs text-muted-foreground">성장하는 팀을 위한 플랜</p></div><div class="mb-6"><span class="text-3xl font-black text-foreground">₩149,000</span><span class="text-sm text-muted-foreground">/월</span></div><ul class="mb-8 flex-1 space-y-3"><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>AI 크레딧 5,000/월</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>전체 AI 모델 (우선 처리)</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>브랜드 보이스 무제한</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>SNS 자동 배포 (전체 채널)</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>팀 협업 (3인)</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>콘텐츠 리퍼포징</li></ul><a class="block rounded-lg py-2.5 text-center text-sm font-medium transition-all border border-border-strong text-secondary-foreground hover:bg-accent" href="https://opadog.site/upgrade">가장 인기 있는 플랜</a></div><div class="relative flex flex-col rounded-2xl border p-6 transition-all hover:scale-[1.02] border-border bg-card"><div class="mb-6"><h3 class="mb-1 text-lg font-bold text-foreground">울트라</h3><p class="text-xs text-muted-foreground">대규모 운영을 위한 플랜</p></div><div class="mb-6"><span class="text-3xl font-black text-foreground">₩293,000</span><span class="text-sm text-muted-foreground">/월</span></div><ul class="mb-8 flex-1 space-y-3"><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>AI 크레딧 10,000/월</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>SNS 인사이트 무제한</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>팀 협업 (무제한)</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>전담 지원</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>우선 처리</li><li class="flex items-start gap-2 text-sm text-secondary-foreground"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>화이트 라벨</li></ul><a class="block rounded-lg py-2.5 text-center text-sm font-medium transition-all border border-border-strong text-secondary-foreground hover:bg-accent" href="https://opadog.site/upgrade">시작하기</a></div></div></div></section><section id="faq" class="relative py-24 px-6"><div class="mx-auto max-w-2xl"><h2 class="mb-14 text-center text-3xl font-bold text-foreground md:text-4xl">자주 묻는 질문</h2><div data-orientation="vertical" dir="ltr" role="region" data-slot="accordion" class="flex w-full flex-col space-y-3"><div data-orientation="vertical" data-index="0" data-closed="" data-slot="accordion-item" class="not-last:border-b rounded-xl border border-border bg-card px-6"><h3 data-orientation="vertical" data-index="0" data-closed="" class="flex"><button type="button" data-value="" data-orientation="vertical" tabindex="0" aria-disabled="false" aria-expanded="false" id="base-ui-_r_8_" data-slot="accordion-trigger" class="group/accordion-trigger relative flex flex-1 items-start justify-between rounded-lg border border-transparent py-2.5 transition-all outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:after:border-ring aria-disabled:pointer-events-none aria-disabled:opacity-50 **:data-[slot=accordion-trigger-icon]:ml-auto **:data-[slot=accordion-trigger-icon]:size-4 **:data-[slot=accordion-trigger-icon]:text-muted-foreground text-left text-base font-medium text-foreground hover:no-underline">정말 5분 만에 콘텐츠를 만들 수 있나요?<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down pointer-events-none shrink-0 group-aria-expanded/accordion-trigger:hidden" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m6 9 6 6 6-6"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-up pointer-events-none hidden shrink-0 group-aria-expanded/accordion-trigger:inline" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m18 15-6-6-6 6"></path></svg></button></h3></div><div data-orientation="vertical" data-index="1" data-closed="" data-slot="accordion-item" class="not-last:border-b rounded-xl border border-border bg-card px-6"><h3 data-orientation="vertical" data-index="1" data-closed="" class="flex"><button type="button" data-value="" data-orientation="vertical" data-index="1" tabindex="0" aria-disabled="false" aria-expanded="false" id="base-ui-_r_b_" data-slot="accordion-trigger" class="group/accordion-trigger relative flex flex-1 items-start justify-between rounded-lg border border-transparent py-2.5 transition-all outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:after:border-ring aria-disabled:pointer-events-none aria-disabled:opacity-50 **:data-[slot=accordion-trigger-icon]:ml-auto **:data-[slot=accordion-trigger-icon]:size-4 **:data-[slot=accordion-trigger-icon]:text-muted-foreground text-left text-base font-medium text-foreground hover:no-underline">영상 편집 경험이 없어도 되나요?<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down pointer-events-none shrink-0 group-aria-expanded/accordion-trigger:hidden" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m6 9 6 6 6-6"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-up pointer-events-none hidden shrink-0 group-aria-expanded/accordion-trigger:inline" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m18 15-6-6-6 6"></path></svg></button></h3></div><div data-orientation="vertical" data-index="2" data-closed="" data-slot="accordion-item" class="not-last:border-b rounded-xl border border-border bg-card px-6"><h3 data-orientation="vertical" data-index="2" data-closed="" class="flex"><button type="button" data-value="" data-orientation="vertical" data-index="2" tabindex="0" aria-disabled="false" aria-expanded="false" id="base-ui-_r_e_" data-slot="accordion-trigger" class="group/accordion-trigger relative flex flex-1 items-start justify-between rounded-lg border border-transparent py-2.5 transition-all outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:after:border-ring aria-disabled:pointer-events-none aria-disabled:opacity-50 **:data-[slot=accordion-trigger-icon]:ml-auto **:data-[slot=accordion-trigger-icon]:size-4 **:data-[slot=accordion-trigger-icon]:text-muted-foreground text-left text-base font-medium text-foreground hover:no-underline">어떤 플랫폼을 지원하나요?<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down pointer-events-none shrink-0 group-aria-expanded/accordion-trigger:hidden" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m6 9 6 6 6-6"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-up pointer-events-none hidden shrink-0 group-aria-expanded/accordion-trigger:inline" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m18 15-6-6-6 6"></path></svg></button></h3></div><div data-orientation="vertical" data-index="3" data-closed="" data-slot="accordion-item" class="not-last:border-b rounded-xl border border-border bg-card px-6"><h3 data-orientation="vertical" data-index="3" data-closed="" class="flex"><button type="button" data-value="" data-orientation="vertical" data-index="3" tabindex="0" aria-disabled="false" aria-expanded="false" id="base-ui-_r_h_" data-slot="accordion-trigger" class="group/accordion-trigger relative flex flex-1 items-start justify-between rounded-lg border border-transparent py-2.5 transition-all outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:after:border-ring aria-disabled:pointer-events-none aria-disabled:opacity-50 **:data-[slot=accordion-trigger-icon]:ml-auto **:data-[slot=accordion-trigger-icon]:size-4 **:data-[slot=accordion-trigger-icon]:text-muted-foreground text-left text-base font-medium text-foreground hover:no-underline">무료 체험은 어떻게 시작하나요?<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down pointer-events-none shrink-0 group-aria-expanded/accordion-trigger:hidden" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m6 9 6 6 6-6"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-up pointer-events-none hidden shrink-0 group-aria-expanded/accordion-trigger:inline" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m18 15-6-6-6 6"></path></svg></button></h3></div><div data-orientation="vertical" data-index="4" data-closed="" data-slot="accordion-item" class="not-last:border-b rounded-xl border border-border bg-card px-6"><h3 data-orientation="vertical" data-index="4" data-closed="" class="flex"><button type="button" data-value="" data-orientation="vertical" data-index="4" tabindex="0" aria-disabled="false" aria-expanded="false" id="base-ui-_r_k_" data-slot="accordion-trigger" class="group/accordion-trigger relative flex flex-1 items-start justify-between rounded-lg border border-transparent py-2.5 transition-all outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:after:border-ring aria-disabled:pointer-events-none aria-disabled:opacity-50 **:data-[slot=accordion-trigger-icon]:ml-auto **:data-[slot=accordion-trigger-icon]:size-4 **:data-[slot=accordion-trigger-icon]:text-muted-foreground text-left text-base font-medium text-foreground hover:no-underline">AI가 만든 콘텐츠의 품질은 어떤가요?<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down pointer-events-none shrink-0 group-aria-expanded/accordion-trigger:hidden" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m6 9 6 6 6-6"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-up pointer-events-none hidden shrink-0 group-aria-expanded/accordion-trigger:inline" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m18 15-6-6-6 6"></path></svg></button></h3></div><div data-orientation="vertical" data-index="5" data-closed="" data-slot="accordion-item" class="not-last:border-b rounded-xl border border-border bg-card px-6"><h3 data-orientation="vertical" data-index="5" data-closed="" class="flex"><button type="button" data-value="" data-orientation="vertical" data-index="5" tabindex="0" aria-disabled="false" aria-expanded="false" id="base-ui-_r_n_" data-slot="accordion-trigger" class="group/accordion-trigger relative flex flex-1 items-start justify-between rounded-lg border border-transparent py-2.5 transition-all outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:after:border-ring aria-disabled:pointer-events-none aria-disabled:opacity-50 **:data-[slot=accordion-trigger-icon]:ml-auto **:data-[slot=accordion-trigger-icon]:size-4 **:data-[slot=accordion-trigger-icon]:text-muted-foreground text-left text-base font-medium text-foreground hover:no-underline">해지는 언제든 가능한가요?<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down pointer-events-none shrink-0 group-aria-expanded/accordion-trigger:hidden" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m6 9 6 6 6-6"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-up pointer-events-none hidden shrink-0 group-aria-expanded/accordion-trigger:inline" aria-hidden="true" data-slot="accordion-trigger-icon"><path d="m18 15-6-6-6 6"></path></svg></button></h3></div></div></div></section><section class="relative py-24 px-6"><div class="mx-auto max-w-4xl overflow-hidden rounded-2xl bg-primary px-8 py-16 text-center md:px-16"><h2 class="mb-4 text-3xl font-bold text-primary-foreground md:text-4xl">지금 바로 시작하세요</h2><p class="mb-8 text-lg text-primary-foreground/90">콘텐츠 자동화의 미래, 오파독AI와 함께</p><button class="inline-block rounded-xl bg-white px-10 py-4 text-lg font-semibold text-primary shadow-lg transition-transform hover:scale-105">무료로 체험하기</button><p class="mt-4 text-sm text-primary-foreground/80">가입 즉시 100 크레딧 무료 · 카드 등록 불필요</p></div></section></main><footer class="border-t border-border py-10 px-6"><div class="mx-auto flex max-w-6xl flex-col items-center gap-4 text-center"><span class="text-lg font-bold"><span class="text-primary">오파독AI</span></span><div class="flex gap-6 text-sm text-muted-foreground"><a class="hover:text-secondary-foreground" href="https://opadog.site/terms">이용약관</a><a class="hover:text-secondary-foreground" href="https://opadog.site/privacy">개인정보처리방침</a><a class="hover:text-secondary-foreground" href="https://opadog.site/contact">문의하기</a></div><address class="flex flex-col gap-1 text-xs not-italic leading-relaxed text-muted-foreground"><span>주식회사 올마이즈 · 대표 김하진</span><span>사업자등록번호 375-87-03241</span><span>서울특별시 동대문구 경희대로 26, 5층 510호(회기동, 삼의원창업센터)</span><span><a href="tel:01032947198" class="hover:text-secondary-foreground">010-3294-7198</a> · <a href="mailto:reukaeim@gmail.com" class="hover:text-secondary-foreground">reukaeim@gmail.com</a></span></address><p class="text-xs text-foreground-faint">© 2026 주식회사 올마이즈. All rights reserved.</p></div></footer></div><section aria-label="Notifications alt+T" tabindex="-1" aria-live="polite" aria-relevant="additions text" aria-atomic="false"></section><script>requestAnimationFrame(function(){$RT=performance.now()});</script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/0486fed93804e349.js.다운로드" id="_R_" async=""></script><script>$RB=[];$RV=function(a){$RT=performance.now();for(var b=0;b<a.length;b+=2){var c=a[b],e=a[b+1];null!==e.parentNode&&e.parentNode.removeChild(e);var f=c.parentNode;if(f){var g=c.previousSibling,h=0;do{if(c&&8===c.nodeType){var d=c.data;if("/$"===d||"/&"===d)if(0===h)break;else h--;else"$"!==d&&"$?"!==d&&"$~"!==d&&"$!"!==d&&"&"!==d||h++}d=c.nextSibling;f.removeChild(c);c=d}while(c);for(;e.firstChild;)f.insertBefore(e.firstChild,c);g.data="$";g._reactRetry&&requestAnimationFrame(g._reactRetry)}}a.length=0};
$RC=function(a,b){if(b=document.getElementById(b))(a=document.getElementById(a))?(a.previousSibling.data="$~",$RB.push(a,b),2===$RB.length&&("number"!==typeof $RT?requestAnimationFrame($RV.bind(null,$RB)):(a=performance.now(),setTimeout($RV.bind(null,$RB),2300>a&&2E3<a?2300-a:$RT+300-a)))):b.parentNode.removeChild(b)};$RC("B:0","S:0")</script><script>(self.__next_f=self.__next_f||[]).push([0])</script><script>self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[22231,[\"/_next/static/chunks/40437a6df375aa7f.js\",\"/_next/static/chunks/72d591b20bc7c2ed.js\",\"/_next/static/chunks/6f797f2a41d8dd2f.js\",\"/_next/static/chunks/a3551492d8356670.js\"],\"Analytics\"]\n5:I[347257,[\"/_next/static/chunks/b59340e5e042fb68.js\"],\"ClientPageRoot\"]\n6:I[422474,[\"/_next/static/chunks/40437a6df375aa7f.js\",\"/_next/static/chunks/72d591b20bc7c2ed.js\",\"/_next/static/chunks/6f797f2a41d8dd2f.js\",\"/_next/static/chunks/a3551492d8356670.js\",\"/_next/static/chunks/47e9aa9c1683ddfb.js\",\"/_next/static/chunks/4d0460a1bf79e696.js\",\"/_next/static/chunks/05eb991dca8618c1.js\",\"/_next/static/chunks/d8ad9666f67919ed.js\",\"/_next/static/chunks/c93d17e2ac482b4c.js\",\"/_next/static/chunks/ea89fd5704e3d7c3.js\",\"/_next/static/chunks/d4a7f7b7002bce64.js\",\"/_next/static/chunks/0ce1fb79df8d30f1.js\",\"/_next/static/chunks/f0467d1e3fd7d5c3.js\"],\"default\"]\n7:I[897367,[\"/_next/static/chunks/b59340e5e042fb68.js\"],\"OutletBoundary\"]\n8:\"$Sreact.suspense\"\na:I[897367,[\"/_next/static/chunks/b59340e5e042fb68.js\"],\"ViewportBoundary\"]\nc:I[897367,[\"/_next/static/chunks/b59340e5e042fb68.js\"],\"MetadataBoundary\"]\ne:I[563491,[\"/_next/static/chunks/3b8b9aef618266ac.js\"],\"default\"]\nf:I[441895,[\"/_next/static/chunks/40437a6df375aa7f.js\",\"/_next/static/chunks/72d591b20bc7c2ed.js\",\"/_next/static/chunks/6f797f2a41d8dd2f.js\",\"/_next/static/chunks/a3551492d8356670.js\"],\"ClientClerkProvider\"]\n10:I[544636,[\"/_next/static/chunks/40437a6df375aa7f.js\",\"/_next/static/chunks/72d591b20bc7c2ed.js\",\"/_next/static/chunks/6f797f2a41d8dd2f.js\",\"/_next/static/chunks/a3551492d8356670.js\"],\"Providers\"]\n11:I[339756,[\"/_next/static/chunks/b59340e5e042fb68.js\"],\"default\"]\n12:I[837457,[\"/_next/static/chunks/b59340e5e042fb68.js\"],\"default\"]\n13:I[713354,[\"/_next/static/chunks/40437a6df375aa7f.js\",\"/_next/static/chunks/72d591b20bc7c2ed.js\",\"/_next/static/chunks/6f797f2a41d8dd2f.js\",\"/_next/static/chunks/a3551492d8356670.js\"],\"Toaster\"]\n14:I[27201,[\"/_next/static/chunks/b59340e5e042fb68.js\"],\"IconMark\"]\n:HL[\"/_next/static/chunks/c9314d0e787cb34f.css\",\"style\"]\n:HL[\"/_next/static/chunks/54252f4f3e444f1a.css\",\"style\"]\n:HL[\"/_next/static/media/5c285b27cdda1fe8-s.p.a62025f2.woff2\",\"font\",{\"crossOrigin\":\"\",\"type\":\"font/woff2\"}]\n:HL[\"/_next/static/media/797e433ab948586e-s.p.29207c2f.woff2\",\"font\",{\"crossOrigin\":\"\",\"type\":\"font/woff2\"}]\n"])</script><script>self.__next_f.push([1,"0:{\"P\":null,\"b\":\"xfY6znyv0JvU7EtYBmY1q\",\"c\":[\"\",\"\"],\"q\":\"\",\"i\":false,\"f\":[[[\"\",{\"children\":[\"(main)\",{\"children\":[\"__PAGE__\",{}]}]},\"$undefined\",\"$undefined\",true],[[\"$\",\"$1\",\"c\",{\"children\":[[[\"$\",\"link\",\"0\",{\"rel\":\"stylesheet\",\"href\":\"/_next/static/chunks/c9314d0e787cb34f.css\",\"precedence\":\"next\",\"crossOrigin\":\"$undefined\",\"nonce\":\"$undefined\"}],[\"$\",\"link\",\"1\",{\"rel\":\"stylesheet\",\"href\":\"/_next/static/chunks/54252f4f3e444f1a.css\",\"precedence\":\"next\",\"crossOrigin\":\"$undefined\",\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-0\",{\"src\":\"/_next/static/chunks/40437a6df375aa7f.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-1\",{\"src\":\"/_next/static/chunks/72d591b20bc7c2ed.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-2\",{\"src\":\"/_next/static/chunks/6f797f2a41d8dd2f.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-3\",{\"src\":\"/_next/static/chunks/a3551492d8356670.js\",\"async\":true,\"nonce\":\"$undefined\"}]],[\"$\",\"html\",null,{\"lang\":\"ko\",\"suppressHydrationWarning\":true,\"children\":[\"$\",\"body\",null,{\"className\":\"dm_sans_45853038-module__6lgKKq__variable geist_mono_8d43a2aa-module__8Li5zG__variable antialiased\",\"children\":[[\"$\",\"$L2\",null,{}],\"$L3\"]}]}]]}],{\"children\":[[\"$\",\"$1\",\"c\",{\"children\":[[[\"$\",\"script\",\"script-0\",{\"src\":\"/_next/static/chunks/47e9aa9c1683ddfb.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-1\",{\"src\":\"/_next/static/chunks/4d0460a1bf79e696.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-2\",{\"src\":\"/_next/static/chunks/05eb991dca8618c1.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-3\",{\"src\":\"/_next/static/chunks/d8ad9666f67919ed.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-4\",{\"src\":\"/_next/static/chunks/c93d17e2ac482b4c.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-5\",{\"src\":\"/_next/static/chunks/ea89fd5704e3d7c3.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-6\",{\"src\":\"/_next/static/chunks/d4a7f7b7002bce64.js\",\"async\":true,\"nonce\":\"$undefined\"}],[\"$\",\"script\",\"script-7\",{\"src\":\"/_next/static/chunks/0ce1fb79df8d30f1.js\",\"async\":true,\"nonce\":\"$undefined\"}]],\"$L4\"]}],{\"children\":[[\"$\",\"$1\",\"c\",{\"children\":[[\"$\",\"$L5\",null,{\"Component\":\"$6\",\"serverProvidedParams\":{\"searchParams\":{},\"params\":{},\"promises\":null}}],[[\"$\",\"script\",\"script-0\",{\"src\":\"/_next/static/chunks/f0467d1e3fd7d5c3.js\",\"async\":true,\"nonce\":\"$undefined\"}]],[\"$\",\"$L7\",null,{\"children\":[\"$\",\"$8\",null,{\"name\":\"Next.MetadataOutlet\",\"children\":\"$@9\"}]}]]}],{},null,false,false]},[[\"$\",\"div\",\"l\",{\"className\":\"flex h-full min-h-[60vh] items-center justify-center\",\"children\":[\"$\",\"div\",null,{\"className\":\"size-6 animate-spin rounded-full border-2 border-border-strong border-t-emerald-400\"}]}],[],[]],false,false]},null,false,false],[\"$\",\"$1\",\"h\",{\"children\":[null,[\"$\",\"$La\",null,{\"children\":\"$Lb\"}],[\"$\",\"div\",null,{\"hidden\":true,\"children\":[\"$\",\"$Lc\",null,{\"children\":[\"$\",\"$8\",null,{\"name\":\"Next.Metadata\",\"children\":\"$Ld\"}]}]}],[\"$\",\"meta\",null,{\"name\":\"next-size-adjust\",\"content\":\"\"}]]}],false]],\"m\":\"$undefined\",\"G\":[\"$e\",[]],\"S\":false}\n"])</script><script>self.__next_f.push([1,"3:[\"$\",\"$Lf\",null,{\"proxyUrl\":\"https://opadog.site/__clerk\",\"appearance\":{\"variables\":{\"colorPrimary\":\"#10b981\"}},\"initialState\":\"$undefined\",\"publishableKey\":\"pk_live_Y2xlcmsub3BhZG9nLnNpdGUk\",\"__internal_clerkJSUrl\":\"$undefined\",\"__internal_clerkJSVersion\":\"$undefined\",\"__internal_clerkUIUrl\":\"$undefined\",\"__internal_clerkUIVersion\":\"$undefined\",\"prefetchUI\":\"$undefined\",\"domain\":\"\",\"isSatellite\":false,\"signInUrl\":\"/sign-in\",\"signUpUrl\":\"/sign-up\",\"signInForceRedirectUrl\":\"\",\"signUpForceRedirectUrl\":\"\",\"signInFallbackRedirectUrl\":\"\",\"signUpFallbackRedirectUrl\":\"\",\"newSubscriptionRedirectUrl\":\"\",\"telemetry\":{\"disabled\":false,\"debug\":false},\"sdkMetadata\":{\"name\":\"@clerk/nextjs\",\"version\":\"7.4.3\",\"environment\":\"production\"},\"unsafe_disableDevelopmentModeConsoleWarning\":false,\"__internal_scriptsSlot\":\"$undefined\",\"children\":[\"$\",\"$L10\",null,{\"children\":[[\"$\",\"$L11\",null,{\"parallelRouterKey\":\"children\",\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$L12\",null,{}],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":[[[\"$\",\"title\",null,{\"children\":\"404: This page could not be found.\"}],[\"$\",\"div\",null,{\"style\":{\"fontFamily\":\"system-ui,\\\"Segoe UI\\\",Roboto,Helvetica,Arial,sans-serif,\\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\"\",\"height\":\"100vh\",\"textAlign\":\"center\",\"display\":\"flex\",\"flexDirection\":\"column\",\"alignItems\":\"center\",\"justifyContent\":\"center\"},\"children\":[\"$\",\"div\",null,{\"children\":[[\"$\",\"style\",null,{\"dangerouslySetInnerHTML\":{\"__html\":\"body{color:#000;background:#fff;margin:0}.next-error-h1{border-right:1px solid rgba(0,0,0,.3)}@media (prefers-color-scheme:dark){body{color:#fff;background:#000}.next-error-h1{border-right:1px solid rgba(255,255,255,.3)}}\"}}],[\"$\",\"h1\",null,{\"className\":\"next-error-h1\",\"style\":{\"display\":\"inline-block\",\"margin\":\"0 20px 0 0\",\"padding\":\"0 23px 0 0\",\"fontSize\":24,\"fontWeight\":500,\"verticalAlign\":\"top\",\"lineHeight\":\"49px\"},\"children\":404}],[\"$\",\"div\",null,{\"style\":{\"display\":\"inline-block\"},\"children\":[\"$\",\"h2\",null,{\"style\":{\"fontSize\":14,\"fontWeight\":400,\"lineHeight\":\"49px\",\"margin\":0},\"children\":\"This page could not be found.\"}]}]]}]}]],[]],\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"}],[\"$\",\"$L13\",null,{}]]}]}]\n"])</script><script>self.__next_f.push([1,"b:[[\"$\",\"meta\",\"0\",{\"charSet\":\"utf-8\"}],[\"$\",\"meta\",\"1\",{\"name\":\"viewport\",\"content\":\"width=device-width, initial-scale=1\"}]]\n9:null\nd:[[\"$\",\"title\",\"0\",{\"children\":\"오파독AI - AI 숏폼 콘텐츠 공장\"}],[\"$\",\"meta\",\"1\",{\"name\":\"description\",\"content\":\"콘텐츠 기획부터 제작까지, AI가 대신합니다. 80+ 전문 스킬로 멀티 플랫폼 콘텐츠를 몇 분 만에 완성하세요.\"}],[\"$\",\"link\",\"2\",{\"rel\":\"icon\",\"href\":\"/favicon.ico?favicon.0b3bf435.ico\",\"sizes\":\"256x256\",\"type\":\"image/x-icon\"}],[\"$\",\"link\",\"3\",{\"rel\":\"icon\",\"href\":\"/icon.png\"}],[\"$\",\"$L14\",\"4\",{}]]\n"])</script><script>self.__next_f.push([1,"15:I[794636,[\"/_next/static/chunks/40437a6df375aa7f.js\",\"/_next/static/chunks/72d591b20bc7c2ed.js\",\"/_next/static/chunks/6f797f2a41d8dd2f.js\",\"/_next/static/chunks/a3551492d8356670.js\",\"/_next/static/chunks/47e9aa9c1683ddfb.js\",\"/_next/static/chunks/4d0460a1bf79e696.js\",\"/_next/static/chunks/05eb991dca8618c1.js\",\"/_next/static/chunks/d8ad9666f67919ed.js\",\"/_next/static/chunks/c93d17e2ac482b4c.js\",\"/_next/static/chunks/ea89fd5704e3d7c3.js\",\"/_next/static/chunks/d4a7f7b7002bce64.js\",\"/_next/static/chunks/0ce1fb79df8d30f1.js\"],\"MainShell\"]\n"])</script><script>self.__next_f.push([1,"4:[\"$\",\"$L15\",null,{\"seed\":{\"role\":\"free\",\"plan\":\"free\",\"enabledFeatures\":[],\"cohort\":null},\"children\":[false,[\"$\",\"$L11\",null,{\"parallelRouterKey\":\"children\",\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$L12\",null,{}],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":[[[\"$\",\"title\",null,{\"children\":\"404: This page could not be found.\"}],[\"$\",\"div\",null,{\"style\":\"$3:props:children:props:children:0:props:notFound:0:1:props:style\",\"children\":[\"$\",\"div\",null,{\"children\":[[\"$\",\"style\",null,{\"dangerouslySetInnerHTML\":{\"__html\":\"body{color:#000;background:#fff;margin:0}.next-error-h1{border-right:1px solid rgba(0,0,0,.3)}@media (prefers-color-scheme:dark){body{color:#fff;background:#000}.next-error-h1{border-right:1px solid rgba(255,255,255,.3)}}\"}}],[\"$\",\"h1\",null,{\"className\":\"next-error-h1\",\"style\":\"$3:props:children:props:children:0:props:notFound:0:1:props:children:props:children:1:props:style\",\"children\":404}],[\"$\",\"div\",null,{\"style\":\"$3:props:children:props:children:0:props:notFound:0:1:props:children:props:children:2:props:style\",\"children\":[\"$\",\"h2\",null,{\"style\":\"$3:props:children:props:children:0:props:notFound:0:1:props:children:props:children:2:props:children:props:style\",\"children\":\"This page could not be found.\"}]}]]}]}]],[]],\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"}]]}]\n"])</script><script src="./오파독AI - AI 숏폼 콘텐츠 공장_files/js" data-nscript="afterInteractive"></script><script id="ga-init" data-nscript="afterInteractive">window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}window.gtag=gtag;gtag('js',new Date());gtag('config','G-GG7LM8GGBK');</script><next-route-announcer style="position: absolute;"><template shadowrootmode="open"><div aria-live="assertive" id="__next-route-announcer__" role="alert" style="position: absolute; border: 0px; height: 1px; margin: -1px; padding: 0px; width: 1px; clip: rect(0px, 0px, 0px, 0px); overflow: hidden; white-space: nowrap; overflow-wrap: normal;"></div></template></next-route-announcer><div id="2fa-auth-scan-qr"><template shadowrootmode="open"><div class="2fa-auth-scan-qr__content" id="2fa-auth-scan-qr__content" data-v-app=""><!----></div></template></div><a id="bottomBar" style="position: fixed; bottom: -40px; left: 0px; z-index: 9999; transform: translateX(-50%); background-color: transparent; border-radius: 5px 5px 0px 0px; opacity: 0.3; padding: 5px; transition: 0.3s; cursor: pointer; max-height: 100px; max-width: 45px;"><img src="chrome-extension://kobncfkmjelbefaoohoblamnbackjggk/icon/icon_32.png" style="width: 32px; height: 32px;"></a><div id="clerk-components"></div></body></html>
import os
import datetime
import pickle
import threading
import sys
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

TOTAL_VIDEOS = 40
VIDEO_DURATION_SEC = 40
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# 프린트되는 글자를 GUI 로그 창으로 보내주는 클래스
class RedirectText:
    def __init__(self, text_ctrl):
        self.output = text_ctrl
    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
    def flush(self):
        pass

def create_daily_image(template_path, new_text, output_path):
    if not os.path.exists(template_path):
        img = Image.new('RGB', (1080, 1920), color=(240, 248, 255))
        d = ImageDraw.Draw(img)
        d.text((100, 100), "No Template Found. Add template.jpg", fill=(255,0,0))
        img.save(template_path)
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("malgun.ttf", 60)
    except:
        font = ImageFont.load_default()
    draw.text((150, 400), new_text, font=font, fill=(0, 0, 0))
    img.save(output_path)

def make_video(image_path, audio_path, output_path, duration=40):
    if not os.path.exists(audio_path):
        from moviepy.audio.AudioClip import AudioArrayClip
        import numpy as np
        silence = AudioArrayClip(np.zeros((44100, 2)), fps=44100).set_duration(duration)
        silence.write_audiofile(audio_path, fps=44100, logger=None)
    img_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)
    if audio_clip.duration > duration:
        audio_clip = audio_clip.subclip(0, duration)
    video = img_clip.set_duration(duration).set_audio(audio_clip)
    video.write_videofile(output_path, fps=1, codec="libx264", audio_codec="aac", logger=None)

def get_authenticated_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secrets.json'):
                print("❌ 오류: 'client_secrets.json' (유튜브 API키) 파일이 필요합니다!")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, video_path, title, upload_date):
    publish_at = upload_date.isoformat() + '.000Z' 
    body = {
        'snippet': {
            'title': title,
            'description': '자동 생성된 금융 꿀팁 영상입니다.',
            'tags': ['재테크', '금융', '자동화'],
            'categoryId': '27'
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': publish_at,
            'selfDeclaredMadeForKids': False
        }
    }
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )
    insert_request.execute()

def run_automation(start_btn):
    start_btn.config(state=tk.DISABLED, text="작업 진행 중...")
    print("="*40)
    print("🚀 유튜브 40일치 영상 일괄 자동화 시작")
    print("="*40)
    
    os.makedirs('output', exist_ok=True)
    os.makedirs('assets', exist_ok=True)
    
    print("인증 정보를 확인하는 중...")
    youtube = get_authenticated_service()
    if not youtube:
        print("작업 취소됨. 세팅을 확인해주세요.")
        start_btn.config(state=tk.NORMAL, text="▶️ 40개 일괄 자동화 시작")
        return
        
    for i in range(TOTAL_VIDEOS):
        upload_date = datetime.datetime.now() + datetime.timedelta(days=i+1)
        topic_title = f"2024년 성공 투자 전략 Part {i+1}"
        image_path = f"output/image_{i}.jpg"
        video_path = f"output/video_{i}.mp4"
        audio_path = "assets/bgm.mp3"
        
        print(f"\n[{i+1}/{TOTAL_VIDEOS}] '{topic_title}' 생성 중...")
        create_daily_image("assets/template.jpg", topic_title, image_path)
        make_video(image_path, audio_path, video_path, VIDEO_DURATION_SEC)
        
        try:
            print("유튜브 예약 업로드 중...")
            upload_video(youtube, video_path, topic_title, upload_date)
            print(f"✅ 업로드 예약 완료 ({upload_date.strftime('%Y-%m-%d')})")
        except Exception as e:
            print(f"❌ 업로드 실패: {e}")
            
    print("\n🎉 모든 작업이 완료되었습니다!")
    start_btn.config(state=tk.NORMAL, text="▶️ 40개 일괄 자동화 시작")

def on_start_click(start_btn):
    # 백그라운드 스레드에서 실행하여 GUI가 멈추지 않도록 함
    threading.Thread(target=run_automation, args=(start_btn,), daemon=True).start()

def main():
    root = tk.Tk()
    root.title("AutoTube - 무인 유튜브 자동화 봇")
    root.geometry("600x450")
    root.configure(padx=20, pady=20)
    
    title_lbl = tk.Label(root, text="🚀 AutoTube AI", font=("Helvetica", 18, "bold"))
    title_lbl.pack(pady=(0, 10))
    
    desc_lbl = tk.Label(root, text="1. assets 폴더에 template.jpg, bgm.mp3 넣기\n2. 현재 폴더에 client_secrets.json 넣기\n이후 아래 버튼을 누르면 자동화가 시작됩니다.", justify=tk.CENTER)
    desc_lbl.pack(pady=(0, 15))
    
    start_btn = tk.Button(root, text="▶️ 40개 일괄 자동화 시작", font=("Helvetica", 14), bg="#764ba2", fg="white", 
                          command=lambda: on_start_click(start_btn))
    start_btn.pack(pady=(0, 20), fill=tk.X, ipady=10)
    
    log_area = scrolledtext.ScrolledText(root, height=12, bg="#f4f4f4", font=("Consolas", 10))
    log_area.pack(fill=tk.BOTH, expand=True)
    
    # print 문이 콘솔이 아닌 GUI 로그 창에 찍히도록 연결
    sys.stdout = RedirectText(log_area)
    sys.stderr = RedirectText(log_area)
    
    print("프로그램이 준비되었습니다. 세팅이 완료되었다면 시작 버튼을 눌러주세요.")
    
    root.mainloop()

if __name__ == '__main__':
    main()

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.ico'],
)

@echo off
chcp 65001 >nul
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [권한 확인] 관리자 권한으로 자동 승격 실행합니다...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title AICHEMI SUB-PC 100% ZERO-TOUCH AUTO-START SETUP
echo ============================================================================
echo [AI Chemi] 보조 노트북 100%% 무인 자동 시작(Auto-Start) 영구 등록
echo ============================================================================

:: 1. 1Gbps 유선 직결 고정 IP (10.0.0.2) 및 방화벽 규칙 적용
netsh interface ip set address name="이더넷" static 10.0.0.2 255.255.255.0 2>nul
netsh interface ip set address name="Ethernet" static 10.0.0.2 255.255.255.0 2>nul
netsh interface ip set address name="이더넷 2" static 10.0.0.2 255.255.255.0 2>nul
netsh interface ip set address name="이더넷 3" static 10.0.0.2 255.255.255.0 2>nul

netsh advfirewall firewall add rule name="AICHEMI_SUB_QA_4000" dir=in action=allow protocol=TCP localport=4000 >nul 2>&1
netsh advfirewall firewall add rule name="AICHEMI_SUB_GPU_5000" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1

powershell -Command "Get-NetConnectionProfile -InterfaceAlias '이더넷*' | Set-NetConnectionProfile -NetworkCategory Private -ErrorAction SilentlyContinue; Get-NetConnectionProfile -InterfaceAlias 'Ethernet*' | Set-NetConnectionProfile -NetworkCategory Private -ErrorAction SilentlyContinue"

echo [1/3] 1Gbps 유선 고정 IP(10.0.0.2) 및 방화벽 포트 4000/5000 영구 개방 완료!

:: 2. Windows 시작 프로그램(Startup) 폴더에 백그라운드 자동 실행 바로가기 등록
powershell -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; $startupDir=[System.IO.Path]::Combine($env:APPDATA, 'Microsoft\Windows\Start Menu\Programs\Startup'); $s=$w.CreateShortcut($startupDir + '\AIChemi_SubPC_AutoDaemon.lnk'); $s.TargetPath='powershell.exe'; $s.Arguments='-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command "Set-Location C:\Users\user\workspace\aichemi; Stop-Process -Name node -Force -ErrorAction SilentlyContinue; node scripts\subpc_orchestrator.js"'; $s.WorkingDirectory='C:\Users\user\workspace\aichemi'; $s.Save()"

echo [2/3] Windows 부팅 시 자동 실행(Startup) 영구 등록 완료!

:: 3. Windows 작업 스케줄러(Task Scheduler) 등록 (야간 03:30 스트레스 테스트 + 04:30 콜드 백업)
powershell -ExecutionPolicy Bypass -File "%~dp0setup_subpc_scheduler.ps1"

echo [3/3] 야간 무인 스트레스 테스트 및 백업 스케줄러 등록 완료!

:: 4. 지금 즉시 백그라운드 데몬 가동
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command "Set-Location C:\Users\user\workspace\aichemi; Stop-Process -Name node -Force -ErrorAction SilentlyContinue; node scripts\subpc_orchestrator.js"' -WindowStyle Hidden"

echo ============================================================================
echo [완료] 이제 보조 컴퓨터를 껐다 켜도 터미널에 명령어를 칠 필요 없이
echo    모든 QA 관제탑 및 워커가 100%% 자동으로 백그라운드에서 실행됩니다!
echo ============================================================================
pause
