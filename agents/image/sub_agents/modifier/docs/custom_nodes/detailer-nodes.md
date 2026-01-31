# 디테일러

**패키지:** comfyui-impact-pack, comfyui-impact-subpack  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md) | [patterns-best-practices](patterns-best-practices.md)

---

## SAMLoader
- 출력: SAM_MODEL. 위젯 model_name, device_mode. 예: `["sam_vit_b_01ec64.pth", "AUTO"]`

**사용 상황**
1. FaceDetailerPipe/EditDetailerPipe에서 더 정확한 마스크가 필요할 때
2. 복잡한 형태(머리카락, 손가락)의 영역을 세그멘트하고 싶을 때
3. sam_vit_b(빠름)/sam_vit_l/sam_vit_h(정확) 중 목적에 맞는 모델을 쓰고 싶을 때
4. ToDetailerPipe에 sam_model_opt로 연결해 디테일러 품질을 높이고 싶을 때
5. VRAM에 맞게 device_mode를 AUTO/CPU 등으로 조정하고 싶을 때
6. YOLO만으로는 영역이 부정확할 때 SAM으로 보완하고 싶을 때
7. 여러 객체가 겹친 장면에서 객체별 마스크가 필요할 때
8. 배경과 전경 분리가 어려울 때 SAM으로 전경 마스크를 만들고 싶을 때
9. Crop By Mask / BatchCropFromMaskAdvanced 전에 정교한 마스크가 필요할 때
10. 실험적으로 SAM 없이(opt) vs SAM 있음으로 품질을 비교하고 싶을 때

---

## UltralyticsDetectorProvider
- 출력: BBOX_DETECTOR, SEGM_DETECTOR. 위젯 model_name
- 옵션: bbox/face_yolov8m.pt(얼굴), bbox/eyes_yolov8n.pt(눈), bbox/hand_yolov8n.pt(손), bbox/body_yolov8m.pt(신체), segm/person_yolov8m-seg.pt(사람)

**사용 상황**
1. 얼굴만 디테일링하고 싶을 때 (face_yolov8m.pt)
2. 눈만 따로 디테일링하고 싶을 때 (eyes_yolov8n.pt) → EditDetailerPipe
3. 손만 따로 디테일링하고 싶을 때 (hand_yolov8n.pt) → EditDetailerPipe
4. 신체/포즈 영역만 디테일링하고 싶을 때 (body_yolov8m.pt)
5. 사람 전체 세그멘트가 필요할 때 (person_yolov8m-seg.pt)
6. ToDetailerPipe에 bbox_detector로 연결해 FaceDetailerPipe/EditDetailerPipe에 쓰고 싶을 때
7. 얼굴 → 눈 → 손 순서로 5단계 디테일링 파이프라인을 만들고 싶을 때
8. 인물 사진/일러스트에서 얼굴·손 품질을 개선하고 싶을 때
9. 여러 인물이 있는 장면에서 각각 얼굴/손을 보정하고 싶을 때
10. bbox vs segm 중 감지 방식에 맞는 모델을 선택하고 싶을 때

---

## ToDetailerPipe
- 입력: model, clip, vae, positive, negative, bbox_detector, sam_model_opt, segm_detector_opt
- 출력: detailer_pipe(DETAILER_PIPE) → FaceDetailerPipe/EditDetailerPipe에 전달

**사용 상황**
1. FaceDetailerPipe/EditDetailerPipe에 넘길 파이프라인을 한 번에 만들고 싶을 때
2. 모델·CLIP·VAE·프롬프트·감지기를 묶어 여러 디테일러 노드에서 재사용하고 싶을 때
3. 얼굴 감지기 + SAM(선택)으로 파이프를 만들고 FaceDetailerPipe에 넘기고 싶을 때
4. EditDetailerPipe에서 감지기만 바꿔 눈/손 등 다른 영역에 같은 파이프를 쓰고 싶을 때
5. 디테일러 전용 모델/프롬프트를 파이프로 고정하고 이미지만 바꿔 쓰고 싶을 때
6. VRAM 절약을 위해 sam_model_opt를 비워 두고 YOLO만 쓰고 싶을 때
7. segm_detector_opt로 세그멘트 감지기를 선택적으로 넣고 싶을 때
8. 동일 설정으로 얼굴 → 눈 → 손 순서 디테일링을 하고 싶을 때
9. 워크플로우 정리를 위해 "디테일러 설정"을 한 노드로 묶고 싶을 때
10. 여러 FaceDetailerPipe/EditDetailerPipe가 같은 파이프를 공유하고 싶을 때

---

## FaceDetailerPipe
- 입력: image(IMAGE), detailer_pipe(DETAILER_PIPE), guide_size(512), max_size(1024), seed, steps, cfg, sampler_name, scheduler, denoise(0.3~0.5), feather, noise_mask, force_inpaint, bbox_threshold(0.5), bbox_dilation, bbox_crop_factor(3.0), sam_*, drop_size, cycle(1~3)
- 출력: IMAGE, cropped_refined, mask, detailer_pipe

**사용 상황**
1. 인물/일러스트에서 얼굴 품질을 개선하고 싶을 때
2. 생성 결과의 얼굴이 흐리거나 왜곡되었을 때 보정하고 싶을 때
3. cycle 1~3으로 반복 보정 강도를 조절하고 싶을 때
4. denoise 0.3~0.5로 원본을 유지하면서 디테일만 보강하고 싶을 때
5. guide_size 512로 얼굴 해상도를 맞춰 품질을 올리고 싶을 때
6. bbox_threshold로 감지 민감도를 조절하고 싶을 때
7. 업스케일 전에 얼굴을 먼저 디테일링하고 싶을 때
8. 여러 인물이 있는 장면에서 각 얼굴을 자동으로 보정하고 싶을 때
9. ToDetailerPipe(얼굴 감지기) + FaceDetailerPipe로 기본 파이프라인을 만들고 싶을 때
10. cropped_refined/mask를 후속 노드에 넘겨 추가 처리하고 싶을 때

---

## EditDetailerPipe
- 입력: detailer_pipe(DETAILER_PIPE), bbox_detector(BBOX_DETECTOR). 출력: detailer_pipe(DETAILER_PIPE)
- 패턴: Face Detector→ToDetailerPipe→FaceDetailerPipe(얼굴); Eyes/Hand Detector→EditDetailerPipe→FaceDetailerPipe(눈/손)

**사용 상황**
1. 기존 파이프의 감지기만 눈(eyes_yolov8n)으로 바꿔 눈만 디테일링하고 싶을 때
2. 기존 파이프의 감지기만 손(hand_yolov8n)으로 바꿔 손만 디테일링하고 싶을 때
3. 얼굴 → 눈 → 손 순서로 같은 파이프를 재사용하고 싶을 때
4. ToDetailerPipe 출력을 EditDetailerPipe(눈 감지기)에 넣고 FaceDetailerPipe에 넘기고 싶을 때
5. FaceDetailerPipe(얼굴) → EditDetailerPipe(손) → FaceDetailerPipe(손) 체인을 만들고 싶을 때
6. 감지기만 여러 개 준비해 같은 모델/프롬프트로 영역별 디테일링하고 싶을 때
7. 눈/손 아티팩트를 영역별로 따로 보정하고 싶을 때
8. 5단계 디테일링(얼굴→눈→얼굴→손→얼굴) 파이프라인을 만들고 싶을 때
9. 워크플로우에서 "파이프는 하나, 감지기만 바꿔 쓰기"를 하고 싶을 때
10. EditDetailerPipe 출력을 다시 FaceDetailerPipe에 넣어 다음 영역을 처리하고 싶을 때
