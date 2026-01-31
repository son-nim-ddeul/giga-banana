# 이미지

**패키지:** comfyui-kjnodes, ComfyUI_Swwan, comfyui-easy-use, rgthree-comfy  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md)

---

## ImageResizeKJ
- 입력: image(IMAGE), width(INT), height(INT), keep_proportion(BOOL), divisible_by(INT)
- 출력: IMAGE, width, height. widgets_values: `[1024, 1024, true, 8]` (8 또는 64 권장)

**사용 상황**
1. 모델/ControlNet 입력 해상도를 8 또는 64 배수로 맞추고 싶을 때
2. 비율을 유지한 채 최대 width/height 안으로 리사이즈하고 싶을 때
3. SD/SDXL 등 모델별 권장 해상도(512, 768, 1024)로 통일하고 싶을 때
4. 업스케일/디테일러 전에 guide_size에 맞춰 리사이즈하고 싶을 때
5. 배치 입력 이미지 크기를 통일하고 싶을 때
6. 출력 해상도(width, height)를 다음 노드(EmptyLatentImage 등)에 넘기고 싶을 때
7. VRAM 절약을 위해 큰 이미지를 1024 이하로 줄이고 싶을 때
8. 여러 소스 이미지를 동일 크기로 맞춰 ImageBatchMulti에 넣고 싶을 때
9. 비율 유지(keep_proportion)와 고정 크기 중 하나를 선택하고 싶을 때
10. divisible_by로 항상 8/64 배수가 되게 해 샘플러 오류를 방지하고 싶을 때

---

## Image Scale By Aspect Ratio v2
- 입력: image(IMAGE), aspect_ratio(STRING). 출력: IMAGE. 위젯 `"16:9"`

**사용 상황**
1. 출력을 16:9, 4:3, 1:1 등 고정 비율로 맞추고 싶을 때
2. 영상/배너용으로 가로형·세로형 비율만 지정하고 싶을 때
3. 원본 비율을 유지한 채 한 변만 맞추고 싶을 때
4. SNS/광고 규격(예: 1:1, 9:16)에 맞춰 리사이즈하고 싶을 때
5. 여러 이미지를 동일 종횡비로 통일하고 싶을 때

---

## ImageBatchMulti
- 입력: image_1, image_2, … (IMAGE). 출력: IMAGE(배치)

**사용 상황**
1. 여러 장을 한 번에 KSampler/VAEDecode에 넣고 배치로 생성하고 싶을 때
2. 서로 다른 소스(LoadImage, 생성 결과 등)를 하나의 배치로 묶고 싶을 때
3. A/B 비교용으로 여러 버전을 한 배치로 모아 저장하고 싶을 때
4. GetImagesFromBatchIndexed와 함께 배치 중 일부만 후처리하고 싶을 때
5. 동일 설정으로 2장, 4장 등 고정 개수만큼 생성하고 싶을 때
6. 여러 프롬프트 결과를 한 번에 Image Saver로 저장하고 싶을 때
7. 디테일러/업스케일 전에 비교할 이미지들을 배치로 묶고 싶을 때
8. 와일드카드 등으로 여러 결과를 낸 뒤 배치로 합쳐 후처리하고 싶을 때

---

## GetImagesFromBatchIndexed
- 입력: images(IMAGE), indexes(STRING). 출력: IMAGE. 위젯 `"0,2,4"`

**사용 상황**
1. 배치에서 특정 인덱스(0번, 2번, 4번)만 골라 후처리하고 싶을 때
2. 여러 결과 중 품질이 좋은 것만 선별해 업스케일/저장하고 싶을 때
3. 배치의 첫 장만(0) 다음 노드로 넘기고 싶을 때
4. 짝수/홀수 인덱스만 따로 처리하고 싶을 때
5. A/B 테스트 결과 중 일부만 저장·비교하고 싶을 때

---

## ColorMatch
- 입력: image(IMAGE), reference(IMAGE), method(COMBO). 출력: IMAGE. method: mkl, hm, reinhard

**사용 상황**
1. 참조 이미지(컨셉아트, 스크린샷)의 색감을 생성 결과에 맞추고 싶을 때
2. 시리즈/에피소드 간 색조를 통일하고 싶을 때
3. 배경과 캐릭터/오브젝트 색을 한 톤으로 맞추고 싶을 때
4. mkl/hm/reinhard 중 목적에 맞는 알고리즘을 선택하고 싶을 때
5. 업스케일/디테일 후 색이 달라졌을 때 원본 톤으로 보정하고 싶을 때
6. 여러 장을 한 장의 분위기에 맞춰 색 보정하고 싶을 때
7. 로그/영화감 필터 느낌을 참조 이미지 기준으로 적용하고 싶을 때
8. 외부 도구에서 만든 이미지와 생성 이미지 색을 맞추고 싶을 때
9. 배치 결과마다 다른 참조로 색을 맞춰 저장하고 싶을 때
10. 최종 출력 전 색 일관성 검사·보정 파이프라인에 넣고 싶을 때

---

## easy imageColorMatch
- 입력: image(IMAGE), reference(IMAGE). 출력: IMAGE

**사용 상황**
1. ColorMatch보다 단순하게 참조 한 장만 연결해 색만 맞추고 싶을 때
2. method 선택 없이 기본 알고리즘만 쓰고 싶을 때
3. 워크플로우를 짧게 유지하면서 색 보정만 넣고 싶을 때
4. 빠른 프리뷰용으로 색 맞춤만 적용하고 싶을 때
5. 참조 이미지가 한 장으로 고정일 때

---

## ImageGridComposite3x3
- 입력: image1~image9(IMAGE). 출력: IMAGE

**사용 상황**
1. 9장의 결과를 3×3 그리드로 합쳐 한 장으로 저장하고 싶을 때
2. 프롬프트/시드 변형 9개를 한눈에 비교하고 싶을 때
3. 스타일 시트·콜라주를 자동으로 만들고 싶을 때
4. 배치 출력을 그리드로 정리해 SNS/문서에 넣고 싶을 때
5. A/B 테스트 그리드, 타일 미리보기 등을 만들고 싶을 때
6. 와일드카드/시드 변형 결과를 한 이미지로 모으고 싶을 때
7. 9장 미만이어도 빈 칸으로 그리드를 만들고 싶을 때(노드 동작에 따름)
8. 동일 구도/다른 스타일 비교용 그리드를 만들고 싶을 때
9. 클라이언트/팀에 선택지 그리드로 보여주고 싶을 때
10. 최종 후보 N장을 3×3으로 묶어 한 번에 저장하고 싶을 때

---

## RgthreeImageComparer
- 입력: image_a, image_b(IMAGE). 출력 없음(UI 비교용)

**사용 상황**
1. 두 장을 나란히 놓고 품질/색/구도를 비교하고 싶을 때
2. 디테일러/업스케일 전후를 UI에서 비교하고 싶을 때
3. 시드/프롬프트만 바꾼 결과를 빠르게 비교하고 싶을 때
4. A/B 테스트 결과를 워크플로우 안에서 바로 확인하고 싶을 때
5. 슬라이더/파라미터 변경 효과를 두 이미지로 비교하고 싶을 때
