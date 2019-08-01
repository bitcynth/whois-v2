#!/bin/bash
VERSION=$(git rev-parse --short HEAD)
echo "$VERSION" > app/version.txt
docker -t whois-app .