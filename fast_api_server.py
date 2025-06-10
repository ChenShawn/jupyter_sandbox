from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

import base64
import argparse
import uvicorn
import time
from PIL import Image
import json

import contextlib
import faulthandler
import io
import multiprocessing
import os
import platform
import signal
import tempfile
from typing import Dict, Optional, Any, List

# jupyter sandbox imports
from IPython.terminal.embed import InteractiveShellEmbed
import io
import redis
import cloudpickle
import base64
import contextlib
import matplotlib.pyplot as plt
from redis_client import RedisClient


def unsafe_execute(check_program: str, timeout: float, result):
    with create_tempdir():

        # These system calls are needed when cleaning up tempdir.
        import os
        import shutil

        rmtree = shutil.rmtree
        rmdir = os.rmdir
        chdir = os.chdir

        # Disable functionalities that can make destructive changes to the test.
        reliability_guard()

        # Construct the check program and run it.
        check_program = check_program

        try:
            exec_globals = {}
            output_stream = io.StringIO()
            with contextlib.redirect_stdout(output_stream):
                with contextlib.redirect_stderr(output_stream):
                    with redirect_stdin(output_stream):
                        with time_limit(timeout):
                            exec(check_program, exec_globals)
            result.append("passed")
            result.append(output_stream.getvalue())
        except TimeoutException:
            result.append("timed out")
        except BaseException as e:
            result.append(f"failed: {e}")

        # Needed for cleaning up.
        shutil.rmtree = rmtree
        os.rmdir = rmdir
        os.chdir = chdir


def check_correctness(
    code_str: str, timeout: float, task_id: Optional[str] = None, completion_id: Optional[int] = None
) -> Dict:
    """
    Evaluates the functional correctness of a completion by running the test
    suite provided in the problem.

    :param completion_id: an optional completion ID so we can match
        the results later even if execution finishes asynchronously.
    """

    manager = multiprocessing.Manager()
    result = manager.list()

    code_str = code_str

    p = multiprocessing.Process(target=unsafe_execute, args=(code_str, timeout, result))
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.kill()

    if not result:
        result.append("timed out")
    
    if len(result) == 1:
        result.append(result[0])

    return dict(
        task_id=task_id,
        passed=result[0] == "passed",
        result=result[1],
        completion_id=completion_id,
    )


@contextlib.contextmanager
def time_limit(seconds: float):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.setitimer(signal.ITIMER_REAL, seconds)
    signal.signal(signal.SIGALRM, signal_handler)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


@contextlib.contextmanager
def create_tempdir():
    with tempfile.TemporaryDirectory() as dirname:
        with chdir(dirname):
            yield dirname


class TimeoutException(Exception):
    pass

class redirect_stdin(contextlib._RedirectStream):  # type: ignore
    _stream = "stdin"


@contextlib.contextmanager
def chdir(root):
    if root == ".":
        yield
        return
    cwd = os.getcwd()
    os.chdir(root)
    try:
        yield
    except BaseException as exc:
        raise exc
    finally:
        os.chdir(cwd)


def reliability_guard(maximum_memory_bytes: Optional[int] = None):
    """
    This disables various destructive functions and prevents the generated code
    from interfering with the test (e.g. fork bomb, killing other processes,
    removing filesystem files, etc.)

    WARNING
    This function is NOT a security sandbox. Untrusted code, including, model-
    generated code, should not be blindly executed outside of one. See the
    Codex paper for more information about OpenAI's code sandbox, and proceed
    with caution.
    """

    if maximum_memory_bytes is not None:
        import resource

        resource.setrlimit(resource.RLIMIT_AS, (maximum_memory_bytes, maximum_memory_bytes))
        resource.setrlimit(resource.RLIMIT_DATA, (maximum_memory_bytes, maximum_memory_bytes))
        if not platform.uname().system == "Darwin":
            resource.setrlimit(resource.RLIMIT_STACK, (maximum_memory_bytes, maximum_memory_bytes))

    faulthandler.disable()

    import builtins

    builtins.exit = None
    builtins.quit = None

    import os

    os.environ["OMP_NUM_THREADS"] = "1"

    os.kill = None
    os.system = None
    os.remove = None
    os.removedirs = None
    os.rmdir = None
    os.fchdir = None
    os.setuid = None
    os.fork = None
    os.forkpty = None
    os.killpg = None
    os.rename = None
    os.renames = None
    os.truncate = None
    os.replace = None
    os.unlink = None
    os.fchmod = None
    os.fchown = None
    os.chmod = None
    os.chown = None
    os.chroot = None
    os.fchdir = None
    os.lchflags = None
    os.lchmod = None
    os.lchown = None
    os.getcwd = None
    os.chdir = None

    import shutil

    shutil.rmtree = None
    shutil.move = None
    shutil.chown = None

    import subprocess

    subprocess.Popen = None  # type: ignore


    import sys

    sys.modules["ipdb"] = None
    sys.modules["joblib"] = None
    sys.modules["resource"] = None
    sys.modules["psutil"] = None
    sys.modules["tkinter"] = None




app = FastAPI()


@app.post("/query")
async def query(request: Request):
    """
    FastAPI endpoint to handle image and text queries.
    """
    # Process the messages


    input_data = await request.json()
    start_time = time.time()

    task_id = input_data.get("task_id")
    code_str = input_data.get("code", "")
    completion_id = input_data.get("completion_id", None)
    timeout = input_data.get("timeout", 5.0)

    result = check_correctness(code_str, timeout, task_id, completion_id)

    execution_time = time.time() - start_time
    response = {
        "output": result,
        "status": "success",
        "execution_time": execution_time
    }

    return response


SAFE_PREFIX = """
import builtins

builtins.exit = None
builtins.quit = None

import os

os.environ["OMP_NUM_THREADS"] = "1"

os.kill = None
os.system = None
os.remove = None
os.removedirs = None
os.rmdir = None
os.fchdir = None
os.setuid = None
os.fork = None
os.forkpty = None
os.killpg = None
os.rename = None
os.renames = None
os.truncate = None
os.replace = None
os.unlink = None
os.fchmod = None
os.fchown = None
os.chmod = None
os.chown = None
os.chroot = None
os.fchdir = None
os.lchflags = None
os.lchmod = None
os.lchown = None
os.getcwd = None
os.chdir = None

import shutil

shutil.rmtree = None
shutil.move = None
shutil.chown = None

import subprocess

subprocess.Popen = None  # type: ignore


import sys

sys.modules["ipdb"] = None
sys.modules["joblib"] = None
sys.modules["resource"] = None
sys.modules["psutil"] = None
sys.modules["tkinter"] = None
"""

RC = RedisClient()

def is_valid_python(code_str: str) -> bool:
    """
    检查给定的 Python 代码字符串是否会导致 SyntaxError。

    :param code_str: 待检查的 Python 代码（字符串）
    :return: 如果会产生 SyntaxError，返回 True；否则返回 False。
    """
    try:
        # 尝试把 code_str 编译成可执行的代码对象
        compile(code_str, '<string>', 'exec')
    except SyntaxError as err:
        return False, str(err)
    else:
        return True, ''

def is_serializable(obj):
    try:
        cloudpickle.dumps(obj)
        return True
    except Exception:
        return False

def save_namespace_to_redis(session_id, user_ns):
    filtered_ns = {
        k: v for k, v in user_ns.items()
        if not k.startswith("__") and is_serializable(v)
    }
    serialized = cloudpickle.dumps(filtered_ns)

    # Set expiration time for 1 hour
    RC.conn.set(session_id, serialized)
    RC.conn.expire(session_id, 3600)
    RC.conn.incr(f"{session_id}--call_cnt")

def get_interactive_shell_from_redis(session_id: str) -> InteractiveShellEmbed:
    """
    Get an InteractiveShellEmbed instance for the given session ID.
    """
    shell = InteractiveShellEmbed()
    data = RC.conn.get(session_id)
    if data:
        user_ns = cloudpickle.loads(data)
        shell.user_ns.update(user_ns)
    else:
        user_ns = {}
        shell.run_cell(SAFE_PREFIX)
        RC.conn.set(f"{session_id}--call_cnt", 0)

    return shell

def run_notebook_code(shell: InteractiveShellEmbed, code: str, timeout: float) -> Dict[str, Any]:
    is_valid, errmsg = is_valid_python(code)
    if not is_valid:
        return {
            'result': None,
            'stdout': '',
            'stderr': f'SyntaxError - {errmsg}',
            'images': []
        }

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    images: List[str] = []
    result = None

    # Temporarily override showtraceback
    original_showtraceback = shell.showtraceback
    def custom_traceback(*args, **kwargs):
        with contextlib.redirect_stdout(stderr_buf):
            return original_showtraceback(*args, **kwargs)

    shell.showtraceback = custom_traceback

    try:
        with contextlib.redirect_stdout(stdout_buf):
            with time_limit(timeout):
                cell = shell.run_cell(code)
                result = getattr(cell, 'result', None)
    finally:
        shell.showtraceback = original_showtraceback

        # Capture matplotlib figures
        for fig_num in plt.get_fignums():
            fig = plt.figure(fig_num)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode('utf-8')
            images.append(img_b64)

    return {
        'result': str(result),
        'stdout': stdout_buf.getvalue(),
        'stderr': stderr_buf.getvalue(),
        'images': images
    }


def jupyter_sandbox_wrapper(session_id: str, code_str: str, timeout: float, final_result):
    shell = get_interactive_shell_from_redis(session_id)
    result = run_notebook_code(shell, code_str, timeout)
    save_namespace_to_redis(session_id, shell.user_ns)
    final_result.append(result)


@app.post("/jupyter_sandbox")
async def jupyter_sandbox(request: Request):
    input_data = await request.json()
    start_time = time.time()

    session_id = str(input_data.get("session_id", "JupyterSandboxDefault"))
    code_str = str(input_data.get("code", ""))
    if code_str.strip() == "":
        return {
            "output": "Error: No code provided",
            "status": "error",
            "execution_time": 0.0,
        }
    timeout = float(input_data.get("timeout", 5.0))

    manager = multiprocessing.Manager()
    result_list = manager.list()

    p = multiprocessing.Process(
        target=jupyter_sandbox_wrapper, 
        args=(session_id, code_str, timeout, result_list)
    )
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.kill()

    if not result_list:
        result_list.append({
            'result': None,
            'stdout': '',
            'stderr': 'TimeOutError: code execution timed out',
            'images': []
        })
    # print(f' [DEBUG fengyuan] {result_list[0]=}')

    execution_time = float(time.time() - start_time)
    response = {
        "output": result_list[0],
        "status": "success",
        "execution_time": execution_time,
    }
    return response


@app.post("/clear_session")
async def jupyter_sandbox(request: Request):
    input_data = await request.json()
    session_id = str(input_data.get("session_id", "JupyterSandboxDefault"))
    RC.conn.expire(session_id, 1)
    return {"status": "success"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FastAPI server for code sandbox.")
    parser.add_argument("--port", type=int, default=12345, help="Port to run the FastAPI server on.")
    args = parser.parse_args()

    uvicorn.run("fast_api_server:app", host="0.0.0.0", port=args.port, reload=False)




