# 유틸리티 (comfyui-custom-scripts, comfyui-kjnodes, comfyui-impact-pack, rgthree-comfy)

## MathExpression|pysssss
- 입력: a, b, c(INT/FLOAT). 출력: INT, FLOAT. 위젯 수식 문자열 예: "a * b + c". 연산 +,-,*,/,%,**, sin, cos, sqrt, min, max, round 등

## SimpleCalculatorKJ
- 입력: a, b(INT/FLOAT), operation(COMBO). 출력: result. operation: add, subtract, multiply, divide, power, modulo

## RgthreeSeed / Seed (rgthree)
- 출력: SEED(INT). 위젯 시드 값. −1=랜덤

## ImpactSwitch
- 입력: select(INT), sel_mode(BOOL), input1~input4(*). 출력: selected(*). 위젯 `[0, false]` (select=0→input1)

## Reroute
- 입출력: 단일 소켓(*). 패스스루

## ImpactWildcardProcessor
- 입력: text(STRING). 출력: STRING. 프롬프트 내 `{A|B|C}` 랜덤 치환

## RgthreePowerPrompt
- 프롬프트 강화 처리

## StringConcatenate
- 입력: 문자열들, 구분자. 출력: STRING
