"""
Render prompt templates with Jinja2, replacing placeholders with real paths.

Usage:
    python3 render_prompts.py <round_num> <project_root> <max_iterations>

Produces rendered prompts in candidates/round_<N>/:
    prompt_search.md
    prompt_verify.md
    prompt_verdict.md
"""

import sys
import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined


def render(round_num, project_root, max_iterations):
    candidates_dir = os.path.join(project_root, 'candidates')
    round_dir = os.path.join(candidates_dir, f'round_{round_num}')
    prev_round_dir = os.path.join(candidates_dir, f'round_{round_num - 1}')
    prev_report = os.path.join(prev_round_dir, 'verification_report.md')

    os.makedirs(round_dir, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(os.path.join(project_root, 'prompts')),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    variables = {
        'round_num': round_num,
        'max_iterations': max_iterations,
        'project_root': project_root,
        'problem_tex': os.path.join(project_root, 'problem.tex'),
        'failed_approaches': os.path.join(candidates_dir, 'failed_approaches.md'),
        'candidate_file': os.path.join(round_dir, 'candidate.py'),
        'candidate_log': os.path.join(round_dir, 'candidate_log.md'),
        'verification_report': os.path.join(round_dir, 'verification_report.md'),
        'prev_report': prev_report if os.path.isfile(prev_report) else None,
    }

    for template_name, output_name in [
        ('search.md', 'prompt_search.md'),
        ('verify.md', 'prompt_verify.md'),
        ('verdict.md', 'prompt_verdict.md'),
    ]:
        template = env.get_template(template_name)
        rendered = template.render(**variables)
        output_path = os.path.join(round_dir, output_name)
        with open(output_path, 'w') as f:
            f.write(rendered)

    # Print the round dir so the shell script can use it
    print(round_dir)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 render_prompts.py <round_num> <project_root> <max_iterations>')
        sys.exit(1)

    render(
        round_num=int(sys.argv[1]),
        project_root=sys.argv[2],
        max_iterations=int(sys.argv[3]),
    )
