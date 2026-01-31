from pathlib import Path


def _read_file(file_path: str) -> str | None:
    """
    내부 파일 읽기 유틸리티 함수.
    파일이 존재하지 않으면 None 반환.
    """
    path = Path(file_path)
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def read_all_custom_nodes_info() -> str | None:
    """
    모든 커스텀 노드들의 역할과 기능 정보를 읽어옵니다.

    Returns:
        str | None: 모든 커스텀 노드들의 역할과 기능 정보 또는 None
    """
    return _read_file("docs/custom_nodes/CUSTOM_NODE_SUMMARY.md")


def read_custom_node_info_details(node_name: str) -> str | None:
    """
    커스텀 노드의 상세 정보를 읽어옵니다.

    Args:
        node_name: 커스텀 노드의 이름

    Returns:
        str | None: 커스텀 노드의 상세 정보 또는 None
    """
    return _read_file(f"docs/custom_nodes/{node_name}.md")


def read_workflow_creation_guide() -> str | None:
    """
    워크플로우 생성 가이드를 읽어옵니다.

    Returns:
        str | None: 워크플로우 생성 가이드 또는 None
    """
    return _read_file("docs/WORKFLOW_CREATION_GUIDE.md")


def read_checkpoint_summary() -> str | None:
    """
    체크포인트 요약 정보를 읽어옵니다.

    Returns:
        str | None: 체크포인트 요약 정보 또는 None
    """
    return _read_file("docs/CHECKPOINT_SUMMARY.md")


def read_checkpoint_info_details(checkpoint_name: str) -> str | None:
    """
    체크포인트의 상세 정보를 읽어옵니다.

    Args:
        checkpoint_name: 체크포인트의 이름

    Returns:
        str | None: 체크포인트의 상세 정보 또는 None
    """
    return _read_file(f"docs/checkpoints/{checkpoint_name}.md")
