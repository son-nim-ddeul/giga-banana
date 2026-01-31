# 유틸리티

**패키지:** comfyui-custom-scripts, comfyui-kjnodes, comfyui-impact-pack, rgthree-comfy  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md)

---

## MathExpression|pysssss
- 입력: a, b, c(INT/FLOAT). 출력: INT, FLOAT. 위젯 수식 문자열 예: "a * b + c". 연산 +,-,*,/,%,**, sin, cos, sqrt, min, max, round 등

**사용 상황**
1. width*2, height*2처럼 해상도를 배수로 계산하고 싶을 때
2. 타일 크기/패딩을 수식으로 계산해 다른 노드에 넘기고 싶을 때
3. 시드/스텝을 a+b 등으로 조합해 동적 값으로 쓰고 싶을 때
4. min(width, 1024)처럼 상한을 두고 싶을 때
5. 비율(scale)을 적용한 크기를 한 줄 수식으로 만들고 싶을 때
6. 여러 입력을 sqrt(a**2 + b**2) 등으로 합쳐 쓰고 싶을 때
7. round(), floor 등으로 정수화해 INT 입력에 넘기고 싶을 때
8. 실험용으로 "a * b + c"만 바꿔 다양한 값을 만들고 싶을 때
9. SimpleCalculatorKJ로는 불가한 복잡한 수식을 쓰고 싶을 때
10. 배치 인덱스/카운터를 수식으로 변환해 파일명/경로에 쓰고 싶을 때

---

## SimpleCalculatorKJ
- 입력: a, b(INT/FLOAT), operation(COMBO). 출력: result. operation: add, subtract, multiply, divide, power, modulo

**사용 상황**
1. 두 값만 더하거나 곱해 다른 노드에 넘기고 싶을 때
2. operation을 드롭다운으로 골라 add/subtract/multiply/divide를 바꾸고 싶을 때
3. MathExpression 없이 간단한 연산만 하고 싶을 때
4. width*scale 같은 한 번의 곱셈/나눗셈이 필요할 때
5. 시드+오프셋, 스텝-감소 등 단순 연산이 필요할 때

---

## RgthreeSeed / Seed (rgthree)
- 출력: SEED(INT). 위젯 시드 값. −1=랜덤

**사용 상황**
1. 매 실행마다 다른 결과를 얻고 싶을 때 (−1)
2. 재현용으로 고정 시드를 지정하고 싶을 때 (0 이상)
3. KSampler 등에 시드 한 줄로 넘기고 싶을 때
4. A1111 스타일의 시드 제어를 쓰고 싶을 때
5. 배치별로 시드만 바꿔 여러 결과를 만들고 싶을 때
6. RgthreeContext와 함께 시드를 CONTEXT에 포함하고 싶을 때
7. 실험에서 동일 시드로 다른 설정만 비교하고 싶을 때
8. 자동화에서 −1로 랜덤 시드를 쓰고 싶을 때
9. 메타데이터(Image Saver)에 시드를 남기고 싶을 때
10. 시드를 수식/다음 노드에 넘겨 파생 값으로 쓰고 싶을 때

---

## ImpactSwitch
- 입력: select(INT), sel_mode(BOOL), input1~input4(*). 출력: selected(*). 위젯 `[0, false]` (select=0→input1)

**사용 상황**
1. VAE 두 개 중 하나를 선택해 VAEDecode에 넘기고 싶을 때
2. positive/negative 두 세트 중 하나를 선택하고 싶을 때
3. 조건(배치 인덱스 등)에 따라 이미지/모델을 바꾸고 싶을 때
4. A/B 테스트로 input1 vs input2를 선택하고 싶을 때
5. 4개까지 후보를 두고 select로 하나만 출력하고 싶을 때
6. Reroute만으로는 분기할 수 없을 때 한 출력만 골라 쓰고 싶을 때
7. 디테일러 on/off처럼 "처리 결과 vs 원본"을 선택하고 싶을 때
8. 업스케일 유무에 따라 다른 경로를 선택하고 싶을 때
9. 타입이 같은 여러 입력 중 인덱스로 하나만 골라 다음 노드에 넘기고 싶을 때
10. 워크플로우에서 "경로 스위치" 하나로 분기를 표현하고 싶을 때

---

## Reroute
- 입출력: 단일 소켓(*). 패스스루

**사용 상황**
1. 긴 연결선을 정리하고 가독성을 높이고 싶을 때
2. 같은 출력을 여러 노드에 나눠 줄 때 중간에 한 번 묶고 싶을 때
3. 노드 위치를 바꿀 때 선이 꼬이지 않게 하고 싶을 때
4. 논리적 그룹(로드/샘플/저장) 사이에 시각적 구분을 두고 싶을 때
5. 타입이 다른 여러 경로를 정리할 때 각각 Reroute로 정리하고 싶을 때

---

## ImpactWildcardProcessor
- 입력: text(STRING). 출력: STRING. 프롬프트 내 `{A|B|C}` 랜덤 치환

**사용 상황**
1. 프롬프트에 `{red|blue|green} dress`처럼 옵션을 넣고 매번 하나만 랜덤 선택하고 싶을 때
2. 배경/시간대/스타일을 `{day|night}`, `{anime|realistic}` 등으로 다양화하고 싶을 때
3. CLIPTextEncode 직전에 와일드카드만 치환하고 싶을 때
4. 여러 시드로 돌릴 때 프롬프트 변형을 자동으로 만들고 싶을 때
5. A/B 테스트용으로 같은 구조에 단어만 바꾼 프롬프트를 쓰고 싶을 때
6. 캐릭터/의상 변형을 한 프롬프트로 여러 버전 생성하고 싶을 때
7. 외부에서 프롬프트 템플릿을 받아 `{placeholder}`만 치환하고 싶을 때
8. 배치 생성 시 매번 다른 옵션이 선택되게 하고 싶을 때
9. 수동으로 여러 프롬프트를 만들지 않고 한 문자열로 다양성 확보하고 싶을 때
10. 트리거 워드/스타일 키워드를 `{style1|style2}`로 넣고 싶을 때

---

## RgthreePowerPrompt
- 프롬프트 강화 처리

**사용 상황**
1. 프롬프트에 가중치/강조를 적용하고 싶을 때
2. rgthree 파이프라인에서 프롬프트 전처리를 한 곳에서 하고 싶을 때
3. A1111 스타일 강화 문법을 쓰고 싶을 때

---

## StringConcatenate
- 입력: 문자열들, 구분자. 출력: STRING

**사용 상황**
1. 파일명을 `prefix_%seed%_%counter%`처럼 조합하고 싶을 때
2. 여러 필드(날짜, 모델명, 시드)를 구분자로 이어 붙이고 싶을 때
3. Image Saver의 filename에 동적 문자열을 넘기고 싶을 때
4. 프롬프트 조각을 구분자 없이/공백으로 이어 붙이고 싶을 때
5. 경로+파일명을 합쳐 저장 경로를 만들고 싶을 때
