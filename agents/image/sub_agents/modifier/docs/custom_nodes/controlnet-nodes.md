# ControlNet 전처리

**패키지:** comfyui_controlnet_aux  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md) | [patterns-best-practices](patterns-best-practices.md)

---

## AIO_Preprocessor
- 입력: preprocessor(COMBO), image(IMAGE), resolution(INT 512 등). 출력: IMAGE
- widgets_values: `["CannyEdgePreprocessor", 512]` 등

**사용 상황**
1. 참조 이미지의 엣지(선)만 추출해 구도를 유지하고 싶을 때 (CannyEdgePreprocessor)
2. 참조 이미지의 포즈(골격)만 추출해 인물 구도를 맞추고 싶을 때 (DWPosePreprocessor)
3. 참조 이미지의 깊이맵을 추출해 3D/레이아웃을 유지하고 싶을 때 (DepthAnythingV2 등)
4. 선화/스케치를 참조해 라인을 유지한 채 채색하고 싶을 때 (LineArtPreprocessor, AnimeLineArtPreprocessor)
5. 만화/일러스트 스타일 선화를 추출하고 싶을 때 (MangaLineArtPreprocessor)
6. 부드러운 엣지가 필요할 때 (HEDPreprocessor)
7. 노멀맵으로 표면 방향을 제어하고 싶을 때 (MiDaS-NormalMapPreprocessor 등)
8. 세그멘트(영역 분리)를 참조로 쓰고 싶을 때 (SegmentAnythingPreprocessor, ColorPreprocessor)
9. 한 노드에서 전처리기 이름만 바꿔 Canny/Depth/Pose 등을 전환하고 싶을 때
10. resolution 512 등으로 전처리 해상도를 맞춰 ControlNet 품질을 조절하고 싶을 때

**전처리기 이름 (preprocessor COMBO)**
- Line: CannyEdgePreprocessor, HEDPreprocessor, LineArtPreprocessor, AnimeLineArtPreprocessor, MangaLineArtPreprocessor, PiDiNetPreprocessor, M-LSDPreprocessor, TEEDPreprocessor, AnyLinePreprocessor
- Depth: MiDaS-DepthMapPreprocessor, Zoe-DepthMapPreprocessor, LeReS-DepthMapPreprocessor, DepthAnythingPreprocessor, DepthAnythingV2Preprocessor, Metric3D-DepthMapPreprocessor
- Normal: MiDaS-NormalMapPreprocessor, BAE-NormalMapPreprocessor, DSINE-NormalMapPreprocessor
- Pose: DWPosePreprocessor(권장), OpenposePreprocessor, MediaPipe-FaceMeshPreprocessor
- Segmentation: SegmentAnythingPreprocessor, ColorPreprocessor, BinaryPreprocessor

**워크플로우**
LoadImage → AIO_Preprocessor(또는 Canny/DWPose 등 개별) → ControlNetLoader → ControlNetApplyAdvanced(positive, negative, control_net, image, strength 0.7~1.0) → CONDITIONING을 KSampler에 연결
