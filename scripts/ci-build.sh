#!/bin/bash

set -e

version="$(git rev-parse --short HEAD)"
tag="$version-$BUILD_NUMBER"

echo "$version" > app/version.txt

docker build -f Dockerfile -t bitcynth/whois-v2:$tag .
docker tag bitcynth/whois-v2:$tag bitcynth/whois-v2:latest
docker push bitcynth/whois-v2:$tag
docker push bitcynth/whois-v2:latest

kubectl set image deployment whois whois=bitcynth/whois-v2:$tag