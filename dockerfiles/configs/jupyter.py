# Very basic configuration, if you want to change the host port
# do so via docker port mapping.
def setup_config():
    c = get_config()
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.port = 8888
    c.NotebookApp.open_browser = False
    c.NotebookApp.token = ''
    c.NotebookApp.allow_root = True

setup_config()