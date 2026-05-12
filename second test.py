# pip install demucs
import subprocess
import os

def separate_stems(input_path, output_dir):
    """
    고품질 모델인 mdx_extra를 사용하여 보컬, 드럼, 베이스, 기타 분리
    """
    try:
        # 워크스테이션의 GPU(CUDA)를 사용하여 분리 실행
        command = f"demucs -n mdx_extra {input_path} -o {output_dir}"
        subprocess.run(command, shell=True, check=True)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# 이후에 FL Studio 3x Osc 프리셋 추천 로직을 여기에 추가할 수 있음