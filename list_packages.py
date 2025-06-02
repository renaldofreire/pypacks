import subprocess

def get_packages(command):
    """Execute a shell command and return the sorted list of packages."""
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
    return sorted(result.stdout.strip().split('\n'))

def format_packages(packages):
    """Format the list of packages into a Markdown table with up to 4 columns."""
    num_cols = 4
    num_pkgs = len(packages)
    num_rows = (num_pkgs + num_cols - 1) // num_cols

    markdown_table = []
    for i in range(num_rows):
        row = "| " + " | ".join(packages[i + j * num_rows] if i + j * num_rows < num_pkgs else "" for j in range(num_cols)) + " |"
        markdown_table.append(row)

    return "\n".join(markdown_table)

def main():
    # Get packages from different sources
    official_pkgs = get_packages("pacman -Qqe | grep -v \"$(pacman -Qqm)\"")
    aur_pkgs = get_packages("pacman -Qqm")
    flatpak_pkgs = get_packages("flatpak list --app --columns=application")

    # Generate Markdown content
    markdown_content = """
# Pacotes Instalados no Arch Linux

## Pacotes Oficiais

| Col 1 | Col 2 | Col 3 | Col 4 |
|----------|----------|----------|----------|
{official_pkgs}

## Pacotes AUR

| Col 1 | Col 2 | Col 3 | Col 4 |
|----------|----------|----------|----------|
{aur_pkgs}

## Pacotes Flatpak

| Col 1 | Col 2 | Col 3 | Col 4 |
|----------|----------|----------|----------|
{flatpak_pkgs}
""".format(
        official_pkgs=format_packages(official_pkgs),
        aur_pkgs=format_packages(aur_pkgs),
        flatpak_pkgs=format_packages(flatpak_pkgs)
    )

    # Save to a Markdown file
    with open("packages_list.md", "w") as md_file:
        md_file.write(markdown_content)

if __name__ == "__main__":
    main()

