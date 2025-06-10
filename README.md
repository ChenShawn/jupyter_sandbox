## Introduction

Yet another code sandbox，但是是jupyter notebook风格的
- 可以像jupyter notebook一样，在同一个session中多次执行代码，下次跑代码的时候可以直接用上次代码中定义的变量；
- 可以像jupyter notebook一样，支持在代码中用`plt.show`输出图片，图片会转成base64格式返回；
- 像jupyter notebook一样，最后一行代码如果没有左值，变量的输出结果会直接在`result`字段中输出；
- 没有搞docker虚拟化，安全起见用HumanEval评测代码中的安全代码包了一层；

## Input Params
- `session_id`: the unique id to identify a specific ipython interactive session
- `code`: python code (type: string) to be executed in the sandbox
- `timeout`: maximum time (seconds) that the python code is allowed to be executed

## Output Params
Upon successful execution, the execution result will be put into `output` field
- result
- stdout
- stderr
- images: base64 format
