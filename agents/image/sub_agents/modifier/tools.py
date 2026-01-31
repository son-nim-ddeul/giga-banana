from pathlib import Path

# modifier 패키지 기준 docs 디렉터리 (cwd 무관)
_DOCS_DIR = Path(__file__).resolve().parent / "docs"

# 유저 상호작용용 노드 상세 문서 (유저에게 값을 받을 수 있는 노드만)
USER_INTERACTION_NODE_DETAIL_NAMES = (
    "file-path-loaders",
    "lora-nodes",
    "image-nodes",
    "mask-crop-nodes",
    "detailer-nodes",
    "upscale-nodes",
    "controlnet-nodes",
)

# 워크플로우 최적화용 노드 상세 문서 (내부 구조·연결·패턴)
OPTIMIZATION_NODE_DETAIL_NAMES = (
    "pipeline-context-nodes",
    "utility-nodes",
    "metadata-save-nodes",
    "patterns-best-practices",
)


def _read_docs_file(relative_path: str) -> str | None:
    """
    docs 디렉터리 기준 상대 경로로 파일을 읽습니다.
    파일이 존재하지 않으면 None 반환.
    """
    path = _DOCS_DIR / relative_path
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def read_user_interaction_nodes_info() -> str | None:
    """
    유저와 상호작용할 노드(유저에게 값을 받을 수 있는 노드) 요약 정보를 읽어옵니다.
    image_modifier 에이전트가 요구사항 구체화 시 참고합니다.

    Returns:
        str | None: 유저 상호작용 노드 요약 또는 None
    """
    return _read_docs_file("USER_INTERACTION_NODE_SUMMARY.md")


def read_user_interaction_node_details(node_name: str) -> str | None:
    """
    유저 상호작용용 노드의 상세 정보를 읽어옵니다.
    허용 문서: file-path-loaders, lora-nodes, image-nodes, mask-crop-nodes,
    detailer-nodes, upscale-nodes, controlnet-nodes.

    Args:
        node_name: 노드 상세 문서 이름 (예: file-path-loaders, lora-nodes)

    Returns:
        str | None: 상세 정보 또는 None (허용 목록 외 이름이면 None)
    """
    if node_name not in USER_INTERACTION_NODE_DETAIL_NAMES:
        return None
    return _read_docs_file(f"custom_nodes/{node_name}.md")


def read_optimization_nodes_info() -> str | None:
    """
    워크플로우 최적화용 노드(파이프라인·유틸·메타데이터·패턴) 요약 정보를 읽어옵니다.
    image_generator 에이전트가 워크플로우 구성 시 참고합니다.

    Returns:
        str | None: 워크플로우 최적화 노드 요약 또는 None
    """
    return _read_docs_file("OPTIMIZATION_NODE_SUMMARY.md")


def read_optimization_node_details(node_name: str) -> str | None:
    """
    워크플로우 최적화용 노드의 상세 정보를 읽어옵니다.
    허용 문서: pipeline-context-nodes, utility-nodes, metadata-save-nodes,
    patterns-best-practices.

    Args:
        node_name: 노드 상세 문서 이름

    Returns:
        str | None: 상세 정보 또는 None (허용 목록 외 이름이면 None)
    """
    if node_name not in OPTIMIZATION_NODE_DETAIL_NAMES:
        return None
    return _read_docs_file(f"custom_nodes/{node_name}.md")


def read_workflow_creation_guide() -> str | None:
    """
    워크플로우 생성 가이드를 읽어옵니다.

    Returns:
        str | None: 워크플로우 생성 가이드 또는 None
    """
    return _read_docs_file("WORKFLOW_CREATION_GUIDE.md")


def read_checkpoint_summary() -> str | None:
    """
    체크포인트 요약 정보를 읽어옵니다.

    Returns:
        str | None: 체크포인트 요약 정보 또는 None
    """
    return _read_docs_file("CHECKPOINT_SUMMARY.md")


def read_checkpoint_info_details(checkpoint_name: str) -> str | None:
    """
    체크포인트의 상세 정보를 읽어옵니다.

    Args:
        checkpoint_name: 체크포인트의 이름

    Returns:
        str | None: 체크포인트의 상세 정보 또는 None
    """
    return _read_docs_file(f"checkpoints/{checkpoint_name}.md")
