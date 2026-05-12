import os
# torchaudio의 새로운 배포 방식을 끄고 구형(안정적) 방식을 쓰게 함
os.environ["TORCHAUDIO_USE_BACKEND_DISPATCH"] = "0"

import sys
import subprocess


import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("입력 파일이 없습니다.")
        return

    filename = sys.argv[1]
    print(f"--- [AI 엔진] {filename} 분석 및 분리 시작 ---")

    try:
        # 실제 Demucs 명령어를 실행합니다.
        # -n mdx_extra는 고성능 모델 이름입니다.
        # processor.py 내부 수정
# 기존: command = f"py -m demucs.separate -n mdx_extra {filename}"

# 수정: filename 변수 앞뒤에 따옴표 추가
        command = f'py -m demucs.separate -n mdx_extra --shifts=2 "{filename}"'
        subprocess.run(command, shell=True, check=True)
        print("--- [AI 엔진] 분리 완료! ---")
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1) # 오류 발생 시 C++에게 1을 반환

if __name__ == "__main__":
    main()