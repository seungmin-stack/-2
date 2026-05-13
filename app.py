from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware # 추가
from fastapi.responses import FileResponse # 추가
import os
import subprocess
import platform
import subprocess

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
    # 파일 저장 로직
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 1. 여기서 운영체제를 다시 한번 확실히 체크합니다.
    current_os = platform.system()
    if current_os == "Windows":
        exe = "py"
    else:
        exe = "python3" # 리눅스(클라우드타입)는 무조건 python3

    # 2. command 리스트의 첫 번째 항목을 위에서 정한 'exe'로 넣습니다.
    command = [
        exe, "-m", "demucs.separate", 
        "-n", "htdemucs", 
        "--shifts", "1", # 메모리 절약을 위해 1 추천
        "-o", RESULT_DIR, 
        file_path
    ]

    print(f"운영체제 확인: {current_os}")
    print(f"최종 실행 명령어: {' '.join(command)}")

    try:
        # 분리 실행
        subprocess.run(command, check=True)
        
        folder_name = file.filename.rsplit('.', 1)[0]
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
        print(f"실행 에러: {str(e)}")
        return {"status": "Error", "error": str(e)}