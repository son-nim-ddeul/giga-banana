# 워크플로우 최적화 노드 요약

워크플로우 구조·연결·메타데이터 저장 등 **내부 최적화**에 쓰는 노드만 정리했습니다.  
유저와 직접 상호작용할 노드(로더, LoRA, 해상도, ControlNet 등)는 image_modifier 에이전트가 별도로 참고합니다.

## 용도

워크플로우를 **실제로 구성·최적화**할 때 이 문서와 상세 문서를 참고하세요.  
RgthreeContext, 스위치, 유틸, 메타데이터 저장, 패턴·베스트 프랙티스가 해당합니다.

## 패키지 (↔ 상세 문서)

| 패키지 | 최적화 관련 기능 | 상세 문서 |
|--------|------------------|------------|
| rgthree-comfy | RgthreeContext, ContextSwitch, 시드, Reroute, PowerPrompt | [pipeline-context-nodes](custom_nodes/pipeline-context-nodes.md), [utility-nodes](custom_nodes/utility-nodes.md) |
| comfyui-easy-use | easy fullLoader(올인원), pipeline 구성 | [pipeline-context-nodes](custom_nodes/pipeline-context-nodes.md) |
| comfyui-custom-scripts, comfyui-kjnodes, comfyui-impact-pack | 수식, 계산기, 스위치, 와일드카드, 문자열 | [utility-nodes](custom_nodes/utility-nodes.md) |
| comfyui-image-saver, comfyui-lora-manager, ComfyUI-EasyFilePaths | Image Saver, Input Parameters, Save Image LM, Job Tracker | [metadata-save-nodes](custom_nodes/metadata-save-nodes.md) |
| (패턴) | 로딩·이미지 체인·디테일링·업스케일 패턴 | [patterns-best-practices](custom_nodes/patterns-best-practices.md) |

## 노드별 역할 (최적화 관점)

### 파이프라인·컨텍스트 ([pipeline-context-nodes](custom_nodes/pipeline-context-nodes.md))
| 노드 | 최적화 용도 |
|------|-------------|
| RgthreeContext / RgthreeContextBig | MODEL/CLIP/VAE/프롬프트를 CONTEXT 한 줄로 묶어 연결선 정리, 하위 노드 공통 설정 |
| RgthreeContextSwitch | 여러 CONTEXT 중 인덱스로 선택, A/B 테스트·모델 전환 |
| easy fullLoader | 체크포인트/VAE/LoRA/해상도/프롬프트 → PIPE_LINE 한 번에 출력 |

### 유틸 ([utility-nodes](custom_nodes/utility-nodes.md))
| 노드 | 최적화 용도 |
|------|-------------|
| MathExpression\|pysssss | width*2, tile 크기, 시드 연산 등 수식으로 값 계산 |
| SimpleCalculatorKJ | 두 값 연산(add/subtract/multiply/divide) |
| RgthreeSeed | 시드 한 줄로 전달, −1=랜덤 |
| ImpactSwitch | select에 따라 input1~4 중 선택 |
| ImpactWildcardProcessor | {A\|B\|C} 랜덤 치환 |
| Reroute | 패스스루, 연결 정리 |
| RgthreePowerPrompt | 프롬프트 강화 |
| StringConcatenate | 문자열·구분자로 연결 |

### 저장·메타데이터 ([metadata-save-nodes](custom_nodes/metadata-save-nodes.md))
| 노드 | 최적화 용도 |
|------|-------------|
| Image Saver | 플레이스홀더(%date%, %model%, %seed% 등)로 파일명·메타데이터 저장 |
| Input Parameters (Image Saver) | steps, cfg, sampler, seed → METADATA로 Image Saver에 연결 |
| Save Image LM | 이미지 + LoRA 정보 메타데이터 저장 |
| Easy JSON Job Tracker | get_next/mark_done/add_job로 작업 큐 관리 |

### 패턴·베스트 프랙티스 ([patterns-best-practices](custom_nodes/patterns-best-practices.md))
- 로딩 패턴(CheckpointLoader vs Easy Checkpoint Loader, LoRA 조합)
- 이미지 체인(기본 / hiresFix / 디테일 / 전체)
- 디테일링(얼굴, 얼굴+눈, denoise/cycle)
- 업스케일·색보정·저장 순서

## 상세 문서 목록 (워크플로우 최적화용)

- [pipeline-context-nodes](custom_nodes/pipeline-context-nodes.md)
- [utility-nodes](custom_nodes/utility-nodes.md)
- [metadata-save-nodes](custom_nodes/metadata-save-nodes.md)
- [patterns-best-practices](custom_nodes/patterns-best-practices.md)
