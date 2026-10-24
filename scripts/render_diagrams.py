"""Render the book's simple Mermaid flowcharts into portable static SVG diagrams.

The generated SVG files work in GitHub Markdown, MkDocs, the locally generated
HTML reader, and in offline environments without JavaScript or a network.

The editable Mermaid source lives in docs/assets/diagrams/*.mmd.
Only graph LR/TD and labeled/unlabeled edges are supported; extend this parser
if you add more advanced Mermaid syntax.

Requirements: Graphviz `dot` command on PATH. Existing SVGs can be used to
read/build the book without Graphviz; dot is only required to regenerate images.
"""
from __future__ import annotations

from pathlib import Path
import re
import math
from xml.sax.saxutils import escape as xml_escape
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "docs" / "assets" / "diagrams"
NODE = r"(?P<{prefix}_id>[A-Za-z][\w]*)(?:\[(?P<{prefix}_text>[^\]]+)\])?"
EDGE = re.compile(r"^\s*" + NODE.format(prefix="src") + r"\s*-->\s*(?:\|(?P<edge>[^|]+)\|\s*)?" + NODE.format(prefix="dst") + r"\s*$")

def dot_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def parse_mermaid(source: str):
    lines=[line.strip() for line in source.splitlines() if line.strip() and not line.lstrip().startswith('%%')]
    match=re.fullmatch(r'(?:graph|flowchart)\s+(LR|TD|TB)',lines[0])
    if not match:
        raise ValueError(f'Unsupported Mermaid graph declaration: {lines[0]}')
    nodes={}
    edges=[]
    for line in lines[1:]:
        m=EDGE.fullmatch(line)
        if not m:
            raise ValueError(f'Unsupported Mermaid edge syntax: {line}')
        for prefix in ('src','dst'):
            node_id,label=m[f'{prefix}_id'],m[f'{prefix}_text']
            if label is not None:
                nodes[node_id]=label
            elif node_id not in nodes:
                nodes[node_id]=node_id
        edges.append((m['src_id'],m['dst_id'],m['edge'] or ''))
    return match.group(1),nodes,edges


def linear_sequence(nodes, edges):
    """Return labels for a simple chain, or None for branches/cycles."""
    if len(edges)!=len(nodes)-1 or any(label for _,_,label in edges):
        return None
    starts=set(nodes)-{b for _,b,_ in edges}
    if len(starts)!=1:
        return None
    start=next(iter(starts))
    nxt={a:b for a,b,_ in edges}
    if len(nxt)!=len(edges):
        return None
    visited=[]
    while start in nodes and start not in visited:
        visited.append(start)
        if start not in nxt:
            break
        start=nxt[start]
    return [nodes[k] for k in visited] if len(visited)==len(nodes) else None


def render_snake_svg(labels, title):
    """Compact two-column flow for long linear diagrams (no JS or images)."""
    rows=math.ceil(len(labels)/2)
    width=708
    height=rows*106+14
    left_x,right_x=22,380
    node_w,node_h=304,60
    coords=[]
    for index in range(len(labels)):
        row=index//2
        col=(index%2) if row%2==0 else 1-(index%2)
        coords.append((left_x if col==0 else right_x,22+row*106))
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{xml_escape(title)}">',
        '<title>'+xml_escape(title)+'</title>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0 0 L8 4 L0 8 Z" fill="#5F7D9A"/></marker></defs>']
    for i in range(len(labels)-1):
        x1,y1=coords[i]; x2,y2=coords[i+1]
        if y1==y2:
            if x1<x2:
                xa,xb=x1+node_w+8,x2-13
            else:
                xa,xb=x1-8,x2+node_w+13
            path=f'M {xa} {y1+node_h/2} L {xb} {y2+node_h/2}'
        else:
            xc=x1+node_w/2
            path=f'M {xc} {y1+node_h+8} L {xc} {y2-13}'
        parts.append(f'<path d="{path}" fill="none" stroke="#5F7D9A" stroke-width="2.2" marker-end="url(#arrow)"/>')
    for i,(label,(x,y)) in enumerate(zip(labels,coords)):
        fill='#DDF1E6' if i==len(labels)-1 else ('#E3F1FC' if i==0 else '#F0F5FC')
        parts.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="13" fill="{fill}" stroke="#ABC5DE" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+node_w/2}" y="{y+36}" text-anchor="middle" font-family="Noto Sans CJK KR, Malgun Gothic, sans-serif" font-size="16" font-weight="550" fill="#203B59">{xml_escape(label)}</text>')
    parts.append('</svg>')
    return '\n'.join(parts)+'\n'


def mermaid_to_dot(source: str) -> str:
    lines = [s.strip() for s in source.splitlines() if s.strip() and not s.lstrip().startswith('%%')]
    match = re.fullmatch(r"(?:graph|flowchart)\s+(LR|TD|TB)", lines[0])
    if not match:
        raise ValueError(f"Unsupported Mermaid graph declaration: {lines[0]}")
    direction = match.group(1)
    nodes: dict[str, str] = {}
    edges: list[tuple[str, str, str]] = []
    for line in lines[1:]:
        m = EDGE.fullmatch(line)
        if not m:
            raise ValueError(f"Unsupported Mermaid edge syntax: {line}")
        for prefix in ('src', 'dst'):
            node_id, label = m[f'{prefix}_id'], m[f'{prefix}_text']
            if label is not None:
                nodes[node_id] = label
            elif node_id not in nodes:
                nodes[node_id] = node_id
        edges.append((m['src_id'], m['dst_id'], m['edge'] or ''))
    # Break long left-to-right chains into a readable, vertical composition.
    # Prioritize legibility in a book column rather than Mermaid's original LR.
    layout = 'TB'
    result = [
        'digraph Diagram {',
        f'  graph [rankdir={layout}, bgcolor="transparent", pad="0.2", nodesep="0.35", ranksep="0.55", splines="polyline"];',
        '  node [shape=box, style="rounded,filled", fontname="Noto Sans CJK KR", fontsize=12, fontcolor="#263D5C", color="#A9C4DB", fillcolor="#EDF4FC", penwidth=1.2, margin="0.26,0.18"];',
        '  edge [color="#617C9C", arrowsize=0.65, penwidth=1.35, fontname="Noto Sans CJK KR", fontsize=10, fontcolor="#425775"];',
    ]
    for i, (key, value) in enumerate(nodes.items()):
        fill = '#E0F1EA' if i == len(nodes) - 1 else ('#E5F2FC' if i == 0 else '#EDF4FC')
        result.append(f'  {key} [label={dot_quote(value)}, fillcolor={dot_quote(fill)}];')
    for a,b,label in edges:
        params=[]
        if label:
            params.append(f'label={dot_quote(label)}')
        if (b,a) in [(u,v) for u,v,_ in edges] and edges.index((a,b,label)) > next(i for i,(u,v,_) in enumerate(edges) if u==b and v==a):
            # Keep the returning fetch/pull arrow separate from the push arrow.
            params.extend(['constraint=false','tailport=e','headport=e'])
        opt=' ['+', '.join(params)+']' if params else ''
        result.append(f'  {a} -> {b}{opt};')
    result.append('}')
    return '\n'.join(result)


def main() -> None:
    dot = shutil.which('dot')
    if not dot:
        raise SystemExit('Graphviz dot not found. Install Graphviz to regenerate diagrams. The SVGs already in docs/assets/diagrams remain usable without it.')
    for path in sorted(DIAGRAMS.glob('*.mmd')):
        original=path.read_text(encoding='utf-8')
        _,nodes,edges=parse_mermaid(original)
        target = path.with_suffix('.svg')
        chain=linear_sequence(nodes,edges)
        if chain and len(chain)>=6:
            target.write_text(render_snake_svg(chain,path.stem.replace('-', ' ')),encoding='utf-8')
        else:
            content=mermaid_to_dot(original)
            result = subprocess.run([dot, '-Tsvg', '-o', str(target)], input=content, encoding='utf-8', capture_output=True)
            if result.returncode:
                raise RuntimeError(f'{path}: {result.stderr}')
        svg = target.read_text(encoding='utf-8')
        if '<svg' not in svg or '</svg>' not in svg:
            raise RuntimeError(f'Invalid SVG: {target}')
        print(f'{target.relative_to(ROOT)} ({target.stat().st_size:,} bytes)')

if __name__ == '__main__':
    main()
