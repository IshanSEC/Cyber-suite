import sys
from core.tool_runner import ToolRunner

def stream_line(line):
    print("STREAM:", line)
    sys.stdout.flush()

runner = ToolRunner()
options = {'extensions': 'php', 'threads': 1, '__output_callback': stream_line}
print("Running dirsearch...")
# run for a fast domain
result = runner.run_tool('dirsearch', 'http://example.com', options)
print("Finished!")
