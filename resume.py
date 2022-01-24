import yaml
import jinja2
import os
import subprocess
import tempfile
import shutil


DATA = "data.yaml"

HEADER_TEMPLATE = "header-template.tex"
RESUME_TEMPLATE = "resume-template.tex"
COVERLETTER_TEMPLATE = "coverletter-template.tex"

HEADER_FILLED = "header-filled.tex"
RESUME_FILLED = "resume-filled.tex"
COVERLETTER_FILLED = "coverletter-filled.tex"

RESUME_OUTPUT = "resume.pdf"
COVERLETTER_OUTPUT = "coverletter.pdf"


def fill_template(data, template):
    with open(data) as f:
        r = yaml.load(f, Loader=yaml.FullLoader)

    latex_env = jinja2.Environment(
        block_start_string="\BLOCK{",
        block_end_string="}",
        variable_start_string="\VAR{",
        variable_end_string="}",
        comment_start_string="\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(".")),
    )
    filledTemplate = latex_env.get_template(template)
    return filledTemplate.render(**r)


def render_latex(filled_file, output_file):
    current = os.getcwd()
    with open(filled_file) as f:
        contents = f.read()

    temp = tempfile.mkdtemp()
    os.chdir(temp)

    print(os.getcwd())

    with open(filled_file, "w") as f:
        f.write(contents)

    subprocess.call(
        [
            "latexmk",
            "-interaction=nonstopmode -file-line-error -lualatex",
            filled_file,
        ]
    )

    pdf_filled_file = filled_file[: filled_file.rindex(".tex")] + ".pdf"
    os.rename(pdf_filled_file, output_file)
    shutil.copy(output_file, current)
    shutil.rmtree(temp)


def fill_all_templates():
    with open(HEADER_FILLED, "w") as f:
        f.write(fill_template(DATA, HEADER_TEMPLATE))

    with open(RESUME_FILLED, "w") as f:
        f.write(fill_template(DATA, RESUME_TEMPLATE))

    with open(COVERLETTER_FILLED, "w") as f:
        f.write(fill_template(DATA, COVERLETTER_TEMPLATE))


def render_all_templates():
    render_latex(RESUME_FILLED, RESUME_OUTPUT)
    render_latex(COVERLETTER_FILLED, COVERLETTER_OUTPUT)


if __name__ == "__main__":
    fill_all_templates()
    render_all_templates()
