serve:
    hugo server --disableFastRender --noHTTPCache --port 1314



# Les livres PDF et EPUB, servis en local depuis static/telechargements/ (ignoré par git)
livre:
    uv run scripts/livre/generer.py
