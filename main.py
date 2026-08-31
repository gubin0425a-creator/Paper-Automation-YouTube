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
