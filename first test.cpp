#include "crow.h"
#include <iostream>
#include <cstdlib>

// 유저의 구독 상태와 남은 횟수를 체크하는 가상 함수
bool check_subscription(std::string user_id) {
    // 실제로는 DB(MySQL/SQLite)에서 조회해야 함
    // 프로 회원이거나 무료 횟수가 남았다면 true
    return true; 
}

int main() {
    crow::SimpleApp app;

    // 1. 오디오 분리 요청 엔드포인트
    CROW_ROUTE(app, "/process_audio").methods(crow::HTTPMethod::POST)
    ([](const crow::request& req) {
        auto user_id = req.url_params.get("user_id");
        
        if (!check_subscription(user_id)) {
            return crow::response(403, "Subscription required or Free limit reached.");
        }

        // 실제 파일 경로 (업로드된 파일)
        std::string input_file = "uploads/track.mp3";
        
        // 2. Python AI 스크립트 실행 (System Call)
        // demucs 모델을 사용하여 분리 명령을 내림
        std::string command = "python3 -m demucs.separate -n mdx_extra " + input_file;
        
        int result = std::system(command.c_str());

        if (result == 0) {
            return crow::response(200, "Processing Complete. Download your stems.");
        } else {
            return crow::response(500, "AI Processing Failed.");
        }
    });

    app.port(8080).multithreaded().run();
}

//py -m uvicorn app:app --reload
