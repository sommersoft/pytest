import argparse
from collections import namedtuple, UserDict
import os
from pprint import pprint
import re
import subprocess

import yaml

parser = argparse.ArgumentParser(
    description="downstream Actions runner"
)
parser.add_argument(
    "repo",
    #nargs=1,
    help="Name of the repo."
)
parser.add_argument(
    "source",
    nargs=1,
    help="Path to source YAML file."
)
parser.add_argument(
    "jobs",
    nargs="+",
    help="Job names to use."
)
parser.add_argument(
    "--matrix-exclude",
    nargs="*",
    default=[],
    help="Exclude these matrix names."
)

def _split_matrix_name_outputs(expr, matrix):
    """ Supply a suitable output for instances of 'split-matrix-name-outputs'
    """
    output = matrix.name.split("-")
    index = int(expr[expr.rfind("_")+1:])
    return output[index]

def _matrix_expr(expr, matrix):
    """ Supply the suitable matrix context variable.
    """
    matrix_key = expr.split(".")[1]
    return matrix._asdict()[matrix_key.strip()]

def _contains(expr, args):
    """ Evaluate if `search` contains `item`
    """
    search = args[0]
    item = args[1]
    return item in search
    
STEP_SUBPARSER_CMDS = {
    "steps.split-matrix-name.outputs._0": _split_matrix_name_outputs,
    "matrix": _matrix_expr,
    "contains": _contains,
}

class ExpressionDispatch(UserDict):
    """ Utility class to dispatch '${{ <expr> }}' expressions to an appropriate handler.
    """
    def __init__(self):
        super().__init__(STEP_SUBPARSER_CMDS)

    def __contains__(self, item):
        if item in self.data:
            return True
        for key in self.data.keys():
            if item.startswith(key):
                return True
        return False

    def dispatch(self, expr, matrix):
        """ Find, call, and return the appropriate expression handler.
        """
        if expr in self.data:
            return self.data[expr](expr, matrix)
        for key in self.data.keys():
            if expr.startswith(key):
                return self.data[key](expr, matrix)
        return expr

STEP_CMD_SUBSTIUTIONS = {
    "systemctl start postgresql.service && postgres createuser --createdb $USER": "/etc/init.d/postgresql start && postgres createuser --createdb $USER",
}

def step_cmd_sub(cmd):
    if cmd not in STEP_CMD_SUBSTIUTIONS:
        return cmd
    return STEP_CMD_SUBSTIUTIONS[cmd]

matrix_nt = namedtuple(
    "matrix",
    ["name", "os", "python", "python_version", "allow_failure"],
    defaults=[None, None, None, None, None]
)

def match_pyenv(version):
    """ Match the pyenv installed full Python version to `version`
    """
    pyenv_versions = subprocess.run(
        ("pyenv", "versions"),
        capture_output=True,
        encoding="utf-8",
        errors="ignore",
        check=True
    )

    for pyenv_version in pyenv_versions.stdout.split("\n"):
        pyenv_version = pyenv_version.lstrip(" *")
        pyenv_version = re.sub(r"\s\(.+\)$", "", pyenv_version)
        if pyenv_version.startswith(version):
            return pyenv_version

class DownstreamRunner:
    # TODO: actualize args vs **kwargs
    def __init__(self, **kwargs):
        with open(kwargs["yaml_source"]) as f:
            self.yaml_tree = yaml.safe_load(f.read())
        
        if self.yaml_tree == None:
            raise SystemExit("Supplied YAML source failed to parse.")

        self.repo = kwargs.get("repo")
        self.matrix_exclude = kwargs.get("matrix_exclude")
        self.job_names = kwargs.get("jobs")
        self._matrix = None
        self._steps = None
        self.expr_dispatcher = ExpressionDispatch()

    def __repr__(self):
        return f"DownstreamRunner(repo={self.repo}, job_names={self.job_names}, matrix={self.matrix}, steps={self.steps})"

    @property
    def matrix(self):
        if self._matrix is None:
            matrix_items = {}
            for job in self.job_names:
                if job not in matrix_items:
                    matrix_items[job] = []
                matrix_items["runs-on"] = self.yaml_tree["jobs"][job].get("runs-on")
                for item in self.yaml_tree["jobs"][job]["strategy"]["matrix"]["include"]:
                    if not item.get("os", "ubuntu").startswith("ubuntu"):
                        continue
                    if item["name"] not in self.matrix_exclude:
                        matrix_items[job].append(
                            matrix_nt(
                                **{
                                    k.replace("-", "_"): v 
                                    for k, v in item.items()
                                }
                            )
                        )
            self._matrix = matrix_items
        return self._matrix

    @property
    def steps(self):
        if self._steps is None:
            step_items = {}
            for job in self.job_names:
                if job not in step_items:
                    step_items[job] = []
                for item in self.yaml_tree["jobs"][job]["steps"]:
                    if "run" in item:
                        step_items[job].append(item)
            self._steps = step_items
        return self._steps
    
    def build_run(self):
        run = {}
        for job in self.job_names:
            for matrix in self.matrix[job]:
                run[matrix.name] = []
                if any([matrix.python, matrix.python_version]):
                    py_version = matrix.python if matrix.python is not None else matrix.python_version
                    run[matrix.name].append({
                        "name": "Set pyenv version",
                        #"run": f"pyenv local {match_pyenv(str(py_version))}\nPYTHONPATH: {os.environ.get('PYTHONPATH')}"
                        "run": f"PYTHONPATH: {os.environ.get('PYTHONPATH')}"
                    })

                for step in self.steps[job]:
                    this_step = step.copy()
                    if "if" in this_step:
                        result = True
                        for expr in re.finditer(r"(?P<func>^.+)\((?P<arg1>.+)\,\s*(?P<arg2>.+)\)", this_step["if"]):
                            func_text = expr.group("func")
                            arg1_text = expr.group("arg1")
                            arg2_text = expr.group("arg2").strip("'")
                            args = []
                            for arg in (arg1_text, arg2_text):
                                if arg in self.expr_dispatcher:
                                    arg = self.expr_dispatcher.dispatch(arg, matrix)
                                args.append(arg)
                            if func_text in self.expr_dispatcher:
                                result = self.expr_dispatcher.dispatch(func_text, args)
                                if not result:
                                    break
                        if not result:
                            continue
                            
                    if "run" in this_step:
                        for expr in re.finditer(r"\${{\s*(?P<expr>.+)\s*}}", this_step["run"]):
                            expr_text = expr.group("expr")
                            if expr_text in self.expr_dispatcher:
                                sub_text = self.expr_dispatcher.dispatch(expr_text, matrix)
                                this_step["run"] = re.sub(r"\${{\s*.+\s*}}", sub_text, this_step["run"])
                        this_step["run"] = this_step["run"].rstrip("\n")
                        this_step["run"] = re.sub(r"sudo\s\-\w+\s|sudo\s", "", this_step["run"])
                    run[matrix.name].append(this_step)
        return run

    def run(self):
        run_steps = self.build_run()
        os.chdir(self.repo)
        for matrix, steps in run_steps.items():
            print(f"::group::{matrix}")
            for step in steps:
                for cmd in step["run"].split("\n"):
                    cmd = step_cmd_sub(cmd).split(" ")
                    print(f"--> running: {cmd}")
                    #continue
                    subprocess.run(
                        cmd,
                        encoding="utf-8",
                        check=True
                    )
            print("::endgroup::")

if __name__ == "__main__":
    cli_args = parser.parse_args()
    runner_args = {
        "repo": cli_args.repo,
        "yaml_source": cli_args.source[0],
        "jobs": cli_args.jobs,
        "matrix_exclude": cli_args.matrix_exclude,
    }
    runner = DownstreamRunner(**runner_args)
    #print(runner)
    #print()
    #pprint(runner.build_run())
    runner.run()
