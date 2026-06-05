import json
from pathlib import Path

PROFILE_PATH = Path(__file__).resolve().parent.parent / "data" / "profile.json"
def load_profile():
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)

def format_list(items):
    return ", ".join(items)

def build_profile_context():
    profile = load_profile()

    projects = "\n".join(
        [
            (
                f"- {project['name']}: {project['description']} "
                f"Technologies: {format_list(project['technologies'])}. "
                f"URL: {project['url']}"
            )
            for project in profile["featured_projects"]
        ]
    )

    links = profile["links"]

    return f"""
            Name: {profile["name"]}
            Background: {format_list(profile["background"])}
            Primary interests: {format_list(profile["primary_interests"])}

            Featured projects:
            {projects}

            Links:
            GitHub: {links["github"]}
            LinkedIn: {links["linkedin"]}
            Portfolio: {links["portfolio"]}
            Email: {links["email"]}
            """