#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <windows.h>

struct User {
    std::string id;
    bool isPro;
    int remainingFreeTrial;
};

void saveUserData(User u) {
    std::ofstream outFile("user_data.txt");
    if (outFile.is_open()) {
        outFile << u.id << " " << u.isPro << " " << u.remainingFreeTrial;
        outFile.close();
    }
}

User loadUserData() {
    std::ifstream inFile("user_data.txt");
    User u = {"music_maker_1", false, 3}; 
    if (inFile.is_open()) {
        inFile >> u.id >> u.isPro >> u.remainingFreeTrial;
        inFile.close();
    }
    return u;
}

int main() {
    SetConsoleOutputCP(65001);
    User currentUser = loadUserData();
    std::string trackName = "lov3.mp3"; // 공백 없는 이름 권장!

    std::cout << "=== 워크스테이션 접속: " << currentUser.id << " ===" << std::endl;

    // 횟수 초과 체크
    if (!currentUser.isPro && currentUser.remainingFreeTrial <= 0) {
        std::cout << "\n[!] 무료 횟수를 모두 사용하셨습니다." << std::endl;
        std::cout << "지금 PRO로 업그레이드하고 무제한 AI 분리를 이용하시겠습니까? (y/n): ";
        
        char choice;
        std::cin >> choice;

        if (choice == 'y' || choice == 'Y') {
            currentUser.isPro = true; // 유저를 PRO로 승격!
            saveUserData(currentUser);
            std::cout << "\n[축하합니다] 이제부터 PRO 멤버십이 적용됩니다! 다시 실행해주세요." << std::endl;
            return 0; 
        } else {
            std::cout << "서비스를 이용하려면 구독이 필요합니다. 종료합니다." << std::endl;
            return 0;
        }
    }

    // AI 처리 로직 (PRO거나 횟수가 남은 경우만 일로 옵니다)
    std::cout << (currentUser.isPro ? "[PRO 상태]" : "[FREE 상태]") << " AI 처리를 시작합니다..." << std::endl;
    
    // 파일 경로에 따옴표 붙이기 (공백 에러 방지)
    std::string command = "py processor.py \"" + trackName + "\"";
    int result = std::system(command.c_str());

    if (result == 0) {
        if (!currentUser.isPro) {
            currentUser.remainingFreeTrial--;
            saveUserData(currentUser);
            std::cout << "남은 횟수: " << currentUser.remainingFreeTrial << "회" << std::endl;
        }
    }

    return 0;
}