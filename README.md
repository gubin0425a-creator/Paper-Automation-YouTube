# AutoTube GitHub Actions

이 폴더에 있는 파일들을 깃허브에 올리면, 깃허브의 클라우드 컴퓨터가 매일 공짜로 영상을 렌더링해서 올려줍니다.

## 세팅 방법
1. https://github.com/new 에 접속해서 새로운 저장소(Repository)를 만듭니다.
2. 이 폴더 안에 있는 모든 파일(`.github` 폴더, `main.py`, `requirements.txt`)을 드래그해서 넣고 Commit 합니다.
3. 레포지토리의 [Settings] -> [Secrets and variables] -> [Actions] 에 들어가서 다음 2가지 시크릿을 추가합니다:
   - `CLIENT_SECRETS_JSON` : 구글 클라우드에서 다운받은 인증 정보
   - `TOKEN_PICKLE_BASE64` : 파이썬으로 최초 로그인 시 생성되는 인증 쿠키 파일
4. [Actions] 탭에서 `AutoTube AI Generator`를 선택하고 [Run workflow]를 누르거나, 넷플리파이 PWA에서 API를 쏴서 자동 실행합니다!
