from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware # 추가
from fastapi.responses import FileResponse # 추가
import os
import subprocess
import platform

app = FastAPI()

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
    # 1단계: 업로드 완료 (10%)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    print(f"분리 시작: {file.filename}")
    
    python_exe = "py" if platform.system() == "Windows" else "python3"
    # 여기서부터 실제 분리 명령
    command = ["py", "-m", "demucs.separate", "-n", "mdx_extra", "--shifts", "2", "-o", RESULT_DIR, file_path]
    
    # 2단계: AI 작업 시작 (이 부분은 시간이 오래 걸리므로 프론트에서 애니메이션 처리)
    result = subprocess.run(command)
    
    if result.returncode == 0:
        # 3단계: 완료 (100%)
        folder_name = file.filename.rsplit('.', 1)[0]
    
    # 작업 실행 (터미널에서 로그를 볼 수 있게 capture_output은 False 권장)
    result = subprocess.run(command)
    
    if result.returncode == 0:
        folder_name = file.filename.rsplit('.', 1)[0]
        base_url = f"/download/mdx_extra/{folder_name}"
        
        return {
            "status": "Success",
            "links": {
                "vocals": f"{base_url}/vocals.wav",
                "drums": f"{base_url}/drums.wav",
                "bass": f"{base_url}/bass.wav",
                "other": f"{base_url}/other.wav"
            }
        }
    else:
        return {"status": "Error", "error": "AI Processing Failed"}