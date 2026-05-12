// 구독 관리 구조체 예시
typedef struct {
    char userId[50];
    int isPro;         // 0: Free, 1: Pro
    int usageCount;    // 이번 달 사용 횟수
    char lastReset[20]; // 마지막 초기화 날짜
} User;

void handleRequest(User *u) {
    if (u->isPro == 1) {
        // 프로는 무제한 & 고음질(FLAC) 처리 모드
        printf("Processing High-Quality Stems for Pro User...\n");
        run_ai_processing("high_res");
    } else {
        if (u->usageCount < 3) {
            // 무료 사용자는 3회 제한 & 저음질(MP3) 처리 모드
            printf("Processing Standard Stems (Free: %d/3)...\n", u->usageCount + 1);
            run_ai_processing("standard");
            u->usageCount++;
        } else {
            printf("Limit Exceeded. Please subscribe to Pro Plan.\n");
        }
    }
}
