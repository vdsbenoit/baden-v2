FROM ubuntu:bionic

LABEL MAINTAINER="Benoit Vander Stappen <vdsbenoit@gmail.com>"

# Based on Kusumoto work https://github.com/Kusumoto/docker-ionic-android-sdk

ARG NODEJS_VERSION="10"
ARG IONIC_VERSION="5.4.12"


# 1) Install system package dependencies
# 2) Install Nodejs/NPM/Ionic-Cli
# 3) Cleanup
# 4) Add and set user for use by ionic and set work folder

RUN apt-get update -qq\
 && apt-get install curl -y \
 && curl -sL https://deb.nodesource.com/setup_${NODEJS_VERSION}.x | bash - \
 && apt-get update \
 && apt-get install -y nodejs \
 && npm install -g @angular/cli \
 && npm install -g firebase-tools \
 && apt-get autoremove -qq\
 && apt-get autoclean \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir /ionicapp

WORKDIR /ionicapp
