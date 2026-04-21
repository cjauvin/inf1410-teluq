"""mdcheck - Vérificateur de liens dans des fichiers Markdown."""

import re
import sys
from pathlib import Path

import requests


def extract_links(text: str) -> list[tuple[str, str]]:
    """Extrait les liens Markdown d'un texte.

    Retourne une liste de tuples (texte, url).
    """
    pattern = r"(?<!!)\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)


def check_url(url: str, timeout: int = 10) -> tuple[bool, str]:
    """Vérifie si une URL est accessible.

    Retourne (True, "OK") ou (False, "message d'erreur").
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code < 400:
            return True, "OK"
        return False, f"HTTP {response.status_code}"
    except requests.ConnectionError:
        return False, "Connexion impossible"
    except requests.Timeout:
        return False, "Timeout"


def check_file(path: Path) -> list[dict]:
    """Vérifie tous les liens dans un fichier Markdown.

    Retourne une liste de résultats pour chaque lien.
    """
    text = path.read_text()
    links = extract_links(text)
    results = []
    for label, url in links:
        if url.startswith("http://") or url.startswith("https://"):
            ok, message = check_url(url)
            results.append(
                {"file": str(path), "label": label, "url": url, "ok": ok, "message": message}
            )
    return results


def main():
    """Point d'entrée principal."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <fichier.md> [fichier2.md ...]")
        sys.exit(1)

    all_ok = True
    for filename in sys.argv[1:]:
        path = Path(filename)
        if not path.exists():
            print(f"Fichier introuvable : {filename}")
            all_ok = False
            continue

        results = check_file(path)
        for r in results:
            status = "✓" if r["ok"] else "✗"
            print(f"  {status} [{r['label']}]({r['url']}) — {r['message']}")
            if not r["ok"]:
                all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
