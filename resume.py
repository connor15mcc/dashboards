import yaml
import jinja2
import os

DATA = "data.yaml"

HEADER_TEMPLATE = "header-template.tex"
RESUME_TEMPLATE = "resume-template.tex"
COVERLETTER_TEMPLATE = "coverletter-template.tex"

HEADER_RENDERED = "header-filled.tex"
RESUME_RENDERED = "resume-filled.tex"
COVERLETTER_RENDERED = "coverletter-filled.tex"


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


if __name__ == "__main__":
    with open(HEADER_RENDERED, "w") as f:
        f.write(fill_template(DATA, HEADER_TEMPLATE))

    with open(RESUME_RENDERED, "w") as f:
        f.write(fill_template(DATA, RESUME_TEMPLATE))

    with open(COVERLETTER_RENDERED, "w") as f:
        f.write(fill_template(DATA, COVERLETTER_TEMPLATE))
