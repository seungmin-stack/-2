from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware # 추가
from fastapi.responses import FileResponse # 추가
import os
import subprocess
import platform
import subprocess
import uuid


app = FastAPI()

# 1. 폴더 생성 로직을 최우선으로 실행
UPLOAD_DIR = "uploads"
RESULT_DIR = "separated"


# 폴더가 없으면 생성 (exist_ok=True로 더 안전하게)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)


# FastAPI 앱 객체 생성 코드 아래에 추가
if not os.path.exists("separated"):
    os.makedirs("separated")
if not os.path.exists("uploads"):
    os.makedirs("uploads")



# ★ CORS 설정 추가: 브라우저 보안 차단 해제
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 도메인 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
RESULT_DIR = "separated"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 정적 파일 경로 등록
app.mount("/download", StaticFiles(directory=RESULT_DIR), name="download")

@app.get("/")
async def read_root():
    return FileResponse('index.html')

@app.post("/separate")
async def upload_music(file: UploadFile = File(...)):
    # 1. 안전한 파일명 생성 (공백/특수문자 제거)
    ext = file.filename.rsplit('.', 1)[-1]
    safe_filename = f"{uuid.uuid4()}.{ext}" # 겹치지 않는 랜덤 이름
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2. 시스템 확인
    exe = "py" if platform.system() == "Windows" else "python3"

    # 3. 메모리 최적화 명령어 (htdemucs + --overlap 0.1)
    command = [
        exe, "-m", "demucs.separate", 
        "-n", "htdemucs", 
        "--shifts", "1",
        "--overlap", "0.1", # 오버랩을 줄여 메모리 사용량 감소
        "-o", RESULT_DIR, 
        file_path
    ]

    try:
        subprocess.run(command, check=True)
        
        # 4. 결과 폴더명은 Demucs가 생성한 이름(확장자 제외 safe_filename) 사용
        folder_name = safe_filename.rsplit('.', 1)[0]
        base_url = f"/download/htdemucs/{folder_name}"
        
        return {
            "status": "Success",
            "links": {
                "vocals": f"{base_url}/vocals.wav",
                "drums": f"{base_url}/drums.wav",
                "bass": f"{base_url}/bass.wav",
                "other": f"{base_url}/other.wav"
            }
        }
    except Exception as e:
        # 에러가 나면 로그에 상세 내용을 찍습니다.
        print(f"Demucs 작업 중 상세 에러: {str(e)}")
        return {"status": "Error", "error": "AI 처리 중 오류가 발생했습니다. 파일이 너무 크거나 메모리가 부족할 수 있습니다."}