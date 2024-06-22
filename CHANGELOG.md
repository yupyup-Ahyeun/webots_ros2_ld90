# Changelog

## 2024.06.03.
- forked from inmo-jang/webots_ros2_ld90
- CHANGELOG.md 생성
- LD90.urdf 수정: main_lidar 옵션 alwaysOn을 true로

## 2024. 06. 05.
- LD90.urdf 수정: DistanceSensor: rear_sornar_1, 2, 3, 4 추가

## 2024. 06. 08.
- 과제 맵(contest.wbt)에 ld90 불러와서 저장
- 과제 맵 설정 옵션 추가

## 2024. 06. 09.
- robot_launch.py 수정: use sim time 및 tf 

## 2024. 06. 10. 
- resource 디렉토리에 nav_params.yaml 추가
- mapping용 사람 없는 맵 contest_non_ped.wbt 추가
- contest_non_ped.wbt 맵 설정 옵션 추가

## 2024. 06. 11.
- universal wheel 참고를 위한 2_wheels_2_universal.wbt 및 2_w_2_u_controller.py 추가
- LD90.proto 수정: 불완전한 caster 교체 완료

## 2024. 06. 12. 
- sang branch를 main branch로 가져옴
- git 변경 --> private 하기 위해

## 2024. 06. 22.
- nav2_params.yaml 파라미터 변형본 업로드
- 함정(맨홀) 없는 맵 추가
- wbt 수정: 로봇 초기화 자세 앞을 보도록 하여 수정
- wbt 수정: WorldInfo에서 contactProperties, slip 일어나지 않도록 수정
