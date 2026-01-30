import json
from pathlib import Path
import argparse
from typing import Any


def export_from_conversation(path: Path, output_dir: Path) -> None:
    with open(path) as f:
        data = json.load(f)

    reports = []
    for convo in data:
        for msg in convo["chat_messages"]:
            for content in msg["content"]:
                if content["type"] == "tool_use" and content["name"] == "artifacts":
                    report = export_artifact_content(content["input"])
                    reports.append((content["input"]["title"], report))

    print(f"Found {len(reports)} reports in conversations")
    print("Writing reports to files")
    for title, report in reports:
        file_name = title.lower().replace(" ", "_") + ".md"
    with open(output_dir / file_name, "w") as f:
        f.write(report)


def export_artifact_content(content_input: dict[str, Any]) -> str:
    report = content_input["content"]
    citations_raw = content_input["md_citations"]

    loc_mapping = {}
    for idx, ctt_raw in enumerate(citations_raw):
        end_index = ctt_raw["end_index"]
        url = ctt_raw["url"]
        title = ctt_raw["metadata"]["preview_title"]
        if end_index in loc_mapping:
            loc_mapping[end_index].append((idx, url, title))
        else:
            loc_mapping[end_index] = [(idx, url, title)]

    acc = 0
    for loc, citations in loc_mapping.items():
        citations_str = ""
        for ctt in citations:
            citations_str += f"[{ctt[0]}]({ctt[1]})"
        report = report[: loc + acc] + citations_str + report[loc + acc :]
        acc += len(citations_str)
        # print(loc, report[loc-5:loc+5])

    return report


def conversation_file(s: str | None = None) -> Path:
    if not Path(s).exists():
        raise argparse.ArgumentTypeError(f"'{s}' is not a valid file")
    return Path(s)


def main():
    parser = argparse.ArgumentParser(
        description="Export deep research report from a conversation.json file exported from Claude"
    )
    parser.add_argument(
        "--path", "-p", type=conversation_file, help="The path to conversation.json"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Path to output directory that will contain report markdown files",
        default="docs",
    )

    args = parser.parse_args()
    if not args.path:
        raise ValueError("must provide a path to a conversation.json file")
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    export_from_conversation(args.path, output_dir)


if __name__ == "__main__":
    main()
