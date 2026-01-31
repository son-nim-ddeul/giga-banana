# ControlNet 전처리 (comfyui_controlnet_aux)

## AIO_Preprocessor
- 입력: preprocessor(COMBO), image(IMAGE), resolution(INT 512 등). 출력: IMAGE
- widgets_values: `["CannyEdgePreprocessor", 512]` 등

## 전처리기 이름 (preprocessor COMBO)
- Line: CannyEdgePreprocessor, HEDPreprocessor, LineArtPreprocessor, AnimeLineArtPreprocessor, MangaLineArtPreprocessor, PiDiNetPreprocessor, M-LSDPreprocessor, TEEDPreprocessor, AnyLinePreprocessor
- Depth: MiDaS-DepthMapPreprocessor, Zoe-DepthMapPreprocessor, LeReS-DepthMapPreprocessor, DepthAnythingPreprocessor, DepthAnythingV2Preprocessor, Metric3D-DepthMapPreprocessor
- Normal: MiDaS-NormalMapPreprocessor, BAE-NormalMapPreprocessor, DSINE-NormalMapPreprocessor
- Pose: DWPosePreprocessor(권장), OpenposePreprocessor, MediaPipe-FaceMeshPreprocessor
- Segmentation: SegmentAnythingPreprocessor, ColorPreprocessor, BinaryPreprocessor

## 워크플로우
LoadImage → AIO_Preprocessor(또는 Canny/DWPose 등 개별) → ControlNetLoader → ControlNetApplyAdvanced(positive, negative, control_net, image, strength 0.7~1.0) → CONDITIONING을 KSampler에 연결
