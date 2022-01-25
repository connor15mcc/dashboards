import yaml
import jinja2
import os
import subprocess
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

LATEX_CLEAN_TYPES = [
    ".aux",
    ".bbl",
    ".blg",
    ".idx",
    ".ind",
    ".lof",
    ".lot",
    ".out",
    ".toc",
    ".acn",
    ".acr",
    ".alg",
    ".glg",
    ".glo",
    ".gls",
    ".fls",
    ".log",
    ".fdb_latexmk",
    ".snm",
    ".synctex(busy)",
    ".synctex.gz(busy)",
    ".nav",
    ".synctex",
    ".synctex.gz",
]


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

    subprocess.call(
        [
            "latexmk",
            "-interaction=nonstopmode",
            "-lualatex",
            filled_file,
        ],
        shell=False,
    )

    pdf_filled_file = filled_file[: filled_file.rindex(".tex")] + ".pdf"
    shutil.move(pdf_filled_file, output_file)


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


def clean_all_build():
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    for file in files:
        if file in [HEADER_FILLED, RESUME_FILLED, COVERLETTER_FILLED]:
            os.remove(file)


def clean_all_aux():
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    for file in files:
        extension = file[file.rindex(".") :]  # noqa: E203
        if extension in LATEX_CLEAN_TYPES:
            os.remove(file)


def main():
    fill_all_templates()
    render_all_templates()
    clean_all_build()
    clean_all_aux()


def update_coverletter(new_name, new_address1, new_address2):
    os.chdir(os.path.dirname(__file__))
    with open(DATA) as f:
        content = yaml.safe_load(f)

    content["coverletter"]["name"] = new_name
    content["coverletter"]["address1"] = new_address1
    content["coverletter"]["address2"] = new_address2

    with open(DATA, "w") as f:
        yaml.dump(content, f, sort_keys=False)

    fill_all_templates()
    render_latex(COVERLETTER_FILLED, COVERLETTER_OUTPUT)
    clean_all_build()
    clean_all_aux()

    content["coverletter"]["name"] = "Company"
    content["coverletter"]["address1"] = "123 Constitution Lane"
    content["coverletter"]["address2"] = "New York, NY 12345"

    with open(DATA, "w") as f:
        yaml.dump(content, f, sort_keys=False)


if __name__ == "__main__":
    main()
