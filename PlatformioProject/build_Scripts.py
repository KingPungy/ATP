Import("env")

"""
This File Contains Custom Build targets for PlatformIO
These can be found in under:

Project Tasks
    |-due
       |-Custom

For extra info about a task hover over the Task in the PlatformIO tab


All Custom Tasks:
 |- Compiling to Assembly .S files
 |- Compiling to Assembly and then running tests
 |- Compiling to Assembly Building src uploading to due and running with monitor
 |- Interpreting the Scolang 
 |- Interpreting the Scolang with Verbose Parsing
 |- Interpreting the Scolang with Verbose and time statistics
 |- Verbose lexing and parsing of the Scolang
"""

env.AddCustomTarget(
    name="gen_assembly",
    dependencies=None,
    actions=[
        "python --version",
        "python main.py ScolangMain.sco -b --compile",
    ],
    title="Build Assembly",
    description="Builds the assembly files from Scolang code",
    always_build= True
) 


"""
   Does exactly the same as the Test task under advanced 
   but builds the assembly files first before running the tests to remove the hassle
"""
env.AddCustomTarget(
    name="gen_asm_test",
    dependencies=None,
    actions=[
        "python --version",
        "python main.py ScolangMain.sco -b --compile",
        "pio test --environment due" # runs test
    ],
    title="Build Assembly and Test",
    description="Builds the assembly files from Scolang code and runs the tests"
) 

env.AddCustomTarget(
    name="gen_asm_run",
    dependencies=None,
    actions=[
        "python --version",
        "python main.py ScolangMain.sco -b --compile",
        "pio run --target upload --target monitor --environment due", # runs and show output in terminal via monitor
    ],
    title="Build Asm Upload Run Monitor",
    description="Builds the assembly files from Scolang code and runs on Due"
) 


env.AddCustomTarget(
    name="Sco_Interpret",
    dependencies=None,
    actions=[
        "python --version",
        "python main.py ScolangMain.sco --interpret"
    ],
    title="Interpret",
    description="Lexes and parses the Scolang code and runs it using the python interpreter"
) 

env.AddCustomTarget(
    name="Sco_Interpret Verbose",
    dependencies=None,
    actions=[
        "python --version",
        "python main.py ScolangMain.sco -v --interpret"
    ],
    title="Interpret Verbose",
    description="Lexes and parses the Scolang code with extra verbose printing and runs it using the python interpreter"
) 

env.AddCustomTarget(
    name="Sco_Interpret Verbose Stats",
    dependencies=None,
    actions=[
        "python --version",
        "python main.py ScolangMain.sco -vs --interpret"
    ],
    title="Interpret Verbose and Statistics",
    description="Lexes and parses the Scolang code with extra verbose printing and time statistics and runs it using the python interpreter"
) 

env.AddCustomTarget(
    name="Sco_Parse verbose",
    dependencies=None,
    actions=[
        "python --version",
        "python main.py ScolangMain.sco -vs"
    ],
    title="Lex & parse Verbose and Statistics",
    description="Lexes and parses the Scolang code with extra verbose printing"
) 


# env.AddCustomTarget(
#     name="pio init",
#     dependencies=None,
#     actions=[
#         "python --version",
#         "pio project init"
#     ],
#     title="Pio init",
#     description="Initializes Platformio Project folder "
# ) 
