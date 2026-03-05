from __future__ import annotations

import base64
from datetime import datetime
from typing import Any

import requests
import streamlit as st

GITHUB_API = "https://api.github.com"


def fetch_public_repos(username: str) -> list[dict[str, Any]]:
    url = f"{GITHUB_API}/users/{username}/repos"
    params = {
        "type": "public",
        "sort": "created",
        "direction": "desc",
        "per_page": 30,
    }
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_readme(owner: str, repo: str) -> str:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/readme"
    headers = {"Accept": "application/vnd.github+json"}
    resp = requests.get(url, headers=headers, timeout=20)
    if resp.status_code == 404:
        return "_No README found._"
    resp.raise_for_status()

    data = resp.json()
    content = data.get("content", "")
    encoding = data.get("encoding", "base64")

    if encoding == "base64":
        try:
            return base64.b64decode(content).decode("utf-8", errors="replace")
        except Exception:
            return "_README exists but could not be decoded._"

    return content or "_README content unavailable._"


def fmt_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return iso


st.set_page_config(page_title="Open Repos Interface", page_icon="📂", layout="wide")
st.title("📂 GitHub Open Repos Interface")
st.caption("Pick your two most recent public repos and browse them in one interface.")

username = st.text_input("GitHub username", value="sarthak-here")

if username.strip():
    try:
        repos = fetch_public_repos(username.strip())
    except Exception as exc:
        st.error(f"Failed to fetch repos: {exc}")
        st.stop()

    if not repos:
        st.warning("No public repos found for this user.")
        st.stop()

    repo_names = [r["name"] for r in repos]
    default_two = repo_names[:2] if len(repo_names) >= 2 else repo_names

    selected = st.multiselect(
        "Choose 2 repos",
        options=repo_names,
        default=default_two,
        max_selections=2,
        help="Select exactly two public repos to compare/view.",
    )

    if len(selected) != 2:
        st.info("Please select exactly 2 repos.")
        st.stop()

    selected_repos = [r for r in repos if r["name"] in selected]
    col1, col2 = st.columns(2)

    for idx, repo in enumerate(selected_repos):
        col = col1 if idx == 0 else col2
        with col:
            st.subheader(repo["name"])
            st.write(repo.get("description") or "_No description_")

            st.markdown(f"**Visibility:** Public")
            st.markdown(f"**Stars:** {repo.get('stargazers_count', 0)}")
            st.markdown(f"**Forks:** {repo.get('forks_count', 0)}")
            st.markdown(f"**Language:** {repo.get('language') or 'N/A'}")
            st.markdown(f"**Created:** {fmt_date(repo.get('created_at', ''))}")
            st.markdown(f"**Updated:** {fmt_date(repo.get('updated_at', ''))}")
            st.markdown(f"🔗 [Open on GitHub]({repo.get('html_url')})")

            with st.expander("README"):
                owner = repo["owner"]["login"]
                readme = fetch_readme(owner, repo["name"])
                st.markdown(readme)

st.divider()
st.caption("Run: `streamlit run ai-projects/open_repos_streamlit.py`")
