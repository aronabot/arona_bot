# 아로나봇(가칭)

## TODO 리스트
- 관리
  - [x] 실시간 extension 로드, 언로드
  - [x] 관리자 관리

- 로깅
  - [ ] 디스코드 채널에 연동된 로깅 
  

- 정보 업데이트 관련 
  - [x] 구글 정보 시트
  - [x] 구글 시트 다운로드
  - [ ] **정보 업데이트 확인** 
  - [x] **정보 업데이트 구현** 
  - [ ] 공식 트위터 연동 

- 데이터
  - [x] 데이터 골격 
  - [ ] 출처 표기
  - [ ] 자주 물어보는 것 (FAQ) 

- 캐릭터
  - [x] 캐릭터 두상 이미지 
  - [x] 캐릭터 능력 정보
  - [x] 캐릭터 스킬 
  - [x] 캐릭터 임베드 출력 
  - [ ] 보정(도시, 실외, 실내) 아이콘 넣기
  - [ ] 다른 특징으로 캐릭터 확인

- 이벤트
  - [ ] 진행중인 이벤트 정보 확인 
  - [x] 진행중인 픽업 정보 확인
  - [ ] 이벤트 히스토리 확인 

- 장비
  - [ ] 장비 파밍 정보 

- 공략
  - [ ] 노말 공략 찾기 
  - [ ] 하드 공략 찾기 

- 미션
  - [ ] 일일 미션 확인 
  - [ ] 주간 미션 확인 

- 기타(옵션)
  - [ ] 도움말 기능
  - [ ] 가챠 기능 
  - [ ] 전술대항전 시뮬레이션 
  - [ ] 로깅을 통한 오류 해결

## reference
- [구글시트](https://docs.google.com/spreadsheets/d/e/2PACX-1vRT3vi_5B6tHsz0s9qGy13-chVMURiogsaz0XXDaGKHPPDok5fRezAoI8NvtHeRqBuvIzmQEMnGr-34/pubhtml), 제작자 [ㅇㅇ](https://gallog.dcinside.com/rodosisland/guestbook), 최종검색일 2021.03.19
- [구글시트](https://docs.google.com/spreadsheets/d/e/2PACX-1vQ4u7GUMO52fMRY1Ndcjvo3MSRiG4FoAYfHzdKLQvVoMAm4wdCnTj-QGLMH2ypE-FRqXaQQLEBUHx4X/pubhtml#), 제작자 [나힝구](https://www.twitch.tv/hinguo8o), 최종검색일 2021.03.17

## 예상 사양  
- !캐릭터 = 캐릭터 목록
- !캐릭터 < X성 > = X성에 해당하는 캐릭터 목록
- !캐릭터 <캐릭터 이름>  = 임베드 캐릭터 정보
- !공략 노말 <지역넘버> = 이미지 공략 정보
- !공략 하드 <지역넘버> = 이미지 공략 정보
- !장비 <장비이름> = 임베드 장비 정보
- !뽑기 <횟수> = 임베드 캐릭터 이미지
- !일일미션 = 이미지 일일미션 번역
- !주간미션 = 이미지 주간미션 번역
- !이벤트 = 현재 진행중인 이벤트
- !총력전 = 현재 진행중인 총력전