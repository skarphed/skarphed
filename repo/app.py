import main

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = main.wsgi_app
    run_simple('scvrepo.freakout.sft.mx', 80, app, use_debugger=True, use_reloader=True)
