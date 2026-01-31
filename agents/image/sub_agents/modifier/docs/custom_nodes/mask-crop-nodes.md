# 마스크·크롭

**패키지:** ComfyUI_Swwan, comfyui-kjnodes  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md) | [patterns-best-practices](patterns-best-practices.md)

---

## Crop By Mask v5
- 입력: image(IMAGE), mask(MASK), padding(INT), force_resize_width/height(INT)
- 출력: IMAGE, crop_box(CROP_BOX), width, height. widgets_values: `[32, 512, 512]`
- 패턴: Image+Mask → Crop By Mask v5 → 처리 → Restore Crop Box v4

**사용 상황**
1. 마스크가 1인 영역만 잘라서 디테일러/업스케일 등 후처리하고 싶을 때
2. 얼굴/손 등 관심 영역만 크롭해 해상도를 올린 뒤 원본에 복원하고 싶을 때
3. VRAM을 아끼기 위해 큰 이미지 중 일부만 처리하고 싶을 때
4. 배경은 유지하고 특정 객체만 수정한 뒤 Restore Crop Box로 합치고 싶을 때
5. SAM/세그멘트 마스크 결과로 영역을 잘라 파이프라인에 넣고 싶을 때
6. padding으로 크롭 범위를 넓혀 경계 아티팩트를 줄이고 싶을 때
7. force_resize로 크롭 영역을 512 등 고정 크기로 맞추고 싶을 때
8. 여러 객체를 BatchCropFromMaskAdvanced로 크롭한 뒤 각각 처리할 때
9. 인페인팅/리터칭 전에 대상 영역만 크롭해 작업하고 싶을 때
10. crop_box를 저장해 동일 위치에 Restore Crop Box로 나중에 합치고 싶을 때

---

## Restore Crop Box v4
- 입력: original_image(IMAGE), cropped_image(IMAGE), crop_box(CROP_BOX), blend_amount(FLOAT)
- 출력: IMAGE. blend_amount 0~1

**사용 상황**
1. Crop By Mask v5로 잘라 처리한 이미지를 원본 크기/위치에 다시 붙이고 싶을 때
2. blend_amount로 경계를 부드럽게 블렌딩하고 싶을 때
3. 디테일러/업스케일 결과를 원본 배경 위에 합성하고 싶을 때
4. 여러 Crop By Mask → 처리 구간을 각각 Restore로 합친 뒤 최종 저장하고 싶을 때
5. 크롭 영역만 바꾼 여러 버전을 원본에 붙여 비교하고 싶을 때

---

## CreateGradientMask
- 입력: width, height(INT), start_x, start_y, end_x, end_y(FLOAT 0~1). 출력: MASK

**사용 상황**
1. 그라데이션 비네팅/페이드 효과를 주고 싶을 때
2. 특정 방향으로만 마스크 강도가 변하는 영역을 만들고 싶을 때
3. 블렌드/합성 시 부드러운 전환 구간을 만들고 싶을 때
4. 상하/좌우로 서서히 사라지는 마스크가 필요할 때
5. 수식/다음 노드와 조합해 동적 그라데이션 마스크를 만들고 싶을 때

---

## CreateShapeMask
- 입력: width, height(INT), shape(COMBO circle/square/triangle), x_pos, y_pos, size(FLOAT 0~1). 출력: MASK

**사용 상황**
1. 원/사각/삼각형 영역만 처리하거나 가리고 싶을 때
2. 포트레이트 중앙(원형)만 디테일/블러하고 싶을 때
3. 로고/워터마크 위치에 도형 마스크를 넣고 싶을 때
4. 인페인팅/리터칭 영역을 도형으로 지정하고 싶을 때
5. x_pos, y_pos, size로 위치·크기를 제어하고 싶을 때
6. 여러 CreateShapeMask를 조합해 복합 마스크를 만들고 싶을 때
7. Crop By Mask 전에 고정 도형 영역을 만들고 싶을 때
8. 테스트/데모용으로 간단한 마스크가 필요할 때
9. 시드/해상도에 따라 동일 비율의 도형 마스크가 필요할 때
10. UI에서 shape를 바꿔 원/사각/삼각을 전환하고 싶을 때

---

## CreateTextMask
- 입력: width, height(INT), text(STRING), font_size(INT), x_pos, y_pos(FLOAT). 출력: MASK

**사용 상황**
1. 텍스트 모양 영역만 인페인팅/색 채우기하고 싶을 때
2. 로고/타이틀 자리에 텍스트 마스크를 넣고 싶을 때
3. 특정 문구 모양으로 마스크를 만들어 합성하고 싶을 때
4. 폰트 크기·위치만 바꿔 여러 텍스트 마스크를 만들고 싶을 때
5. 워터마크 제거/덮기 영역을 텍스트로 지정하고 싶을 때

---

## GrowMaskWithBlur
- 입력: mask(MASK), expand(INT), incremental_expand(BOOL), tapered_corners(BOOL), blur_radius(FLOAT), lerp_alpha(FLOAT). 출력: MASK

**사용 상황**
1. 마스크 경계를 몇 픽셀 넓혀 블렌드 아티팩트를 줄이고 싶을 때
2. 디테일러/인페인팅 전에 마스크를 부드럽게(blur) 확장하고 싶을 때
3. expand로 감지 영역보다 약간 넓게 처리하고 싶을 때
4. tapered_corners로 모서리를 완만히 하고 싶을 때
5. Crop By Mask / FaceDetailer 등에 넣기 전 마스크 전처리로 쓰고 싶을 때
6. SAM/세그멘트 마스크가 너무 딱딱할 때 부드럽게 만들고 싶을 때
7. 여러 마스크를 블렌딩할 때 경계를 blur로 부드럽게 하고 싶을 때
8. lerp_alpha로 마스크 강도/페이드를 조절하고 싶을 때
9. 실험적으로 expand/blur 값을 바꿔 최적값을 찾고 싶을 때
10. Restore Crop Box 직전 블렌드 품질을 높이고 싶을 때

---

## BatchCropFromMaskAdvanced
- 입력: image(IMAGE), mask(MASK), bbox_smooth_alpha(FLOAT), crop_size_mult(FLOAT), bbox_fill(COMBO). 출력: IMAGE(배치), bbox, index

**사용 상황**
1. 한 장의 마스크에서 연결된 영역 여러 개를 각각 크롭해 배치로 만들고 싶을 때
2. 여러 얼굴/객체를 동시에 크롭해 각각 디테일링하고 싶을 때
3. SAM/세그멘트 결과로 여러 객체를 개별 크롭하고 싶을 때
4. crop_size_mult로 크롭 박스에 여유를 주고 싶을 때
5. bbox_fill으로 빈 영역을 border 등으로 채우고 싶을 때
6. 인덱스별로 다른 후처리(얼굴/손 등)를 적용하고 싶을 때
7. 그리드/비교용으로 여러 영역을 한 배치로 모으고 싶을 때
8. bbox를 다른 노드에 넘겨 위치 정보를 활용하고 싶을 때
9. 메모리 효율을 위해 영역별로 순차 처리할 때
10. 여러 인물/오브젝트를 한 번에 크롭해 일괄 저장하고 싶을 때
