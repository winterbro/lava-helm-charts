import json
import os
import requests
import subprocess
from typing import List, Tuple

def get_release_and_pre_release_tags() -> Tuple[List[str], List[str]]:
    tags_env = os.environ['TAGS']
    if tags_env == '':
        print("ERROR: TAGS environment variable is not set.")
        exit(1)

    raw_tags = json.loads(tags_env)
    if len(raw_tags) == 0:
        print("ERROR: TAGS is empty")
        exit(1)

    # only build tags after 0.24
    tags = []
    for tag in raw_tags:
        minor = tag.replace("v", "").split(".")[1]
        minor_int = int(minor)

        if minor_int >= 24:
            tags.append(tag)

    releases = []
    pre_releases = []

    github_release_url = "https://api.github.com/repos/lavanet/lava/releases"

    response = requests.get(github_release_url)
    releases_json = response.json()

    for release in releases_json:
        # create releases list
        if release['tag_name'] in tags and release['draft'] == False and release['prerelease'] == False:
            releases.append(release['tag_name'])

        # create pre-releases list
        if release['tag_name'] in tags and release['draft'] == False and release['prerelease'] == True:
            pre_releases.append(release['tag_name'])

        # break if we have all the tags we need
        if len(releases) + len(pre_releases) == len(tags):
            break

    return releases, pre_releases

def main():
    releases, pre_releases = get_release_and_pre_release_tags()
    latest_release = releases[0]

    # build release versions
    for release in releases:
        build(release)

    # build pre-release versions
    for pre_release in pre_releases:
        build(pre_release, f"pre-{pre_release}")

    # build latest
    build(latest_release, "latest")

def build(version_tag: str, docker_tag = None):
    if docker_tag is None:
        docker_tag = version_tag

    use_cache_env = os.environ.get('USE_CACHE')
    use_cache = use_cache_env != None and use_cache_env != 'false' and use_cache_env != '' and use_cache_env != '0'

    images = [["rpc", "lava-rpc"], ["provider", "lava-provider"]]
    for [dockerfile_path, image_name] in images:
        if docker_tag != "latest" and image_exists_in_repo(image_name, docker_tag):
            print(f"Image {image_name}:{docker_tag} already exists in repository, skipping")
            continue
        else:
            print(f"Building {dockerfile_path} ({image_name}:{docker_tag}): TAG={version_tag}\n")

        args = ["docker", "buildx", "build", ".", "-t", f"us-central1-docker.pkg.dev/lavanet-public/images/{image_name}:{docker_tag}", "--build-arg", f"TAG={version_tag}", "-f", "Dockerfile", "--push"]

        if use_cache:
            args = args + ["--cache-from", "type=local,src=/tmp/.buildx-cache", "--cache-to", "type=local,dest=/tmp/.buildx-cache-new"]

        exit_code = subprocess.Popen(args, cwd=f"dockerfiles/{dockerfile_path}").wait()

        if exit_code != 0:
            print(f"ERROR: Failed to build {image_name}")
            exit(1)

        print(f"Successfully built {image_name}:{docker_tag}\n")

def image_exists_in_repo(image_name: str, tag: str) -> bool:
    args = ["docker", "manifest", "inspect", f"us-central1-docker.pkg.dev/lavanet-public/images/{image_name}:{tag}"]
    exit_code = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

    return exit_code == 0


if __name__ == '__main__':
    main()
