#!/usr/bin/env bash

## Install Dependencies
sudo apt update
sudo apt install -y autoconf automake libtool
sudo apt install -y libpng12-dev
sudo apt install -y libjpeg8-dev
sudo apt install -y libtiff5-dev
sudo apt install -y libjpeg62-dev
sudo apt install -y g++
sudo apt install -y libtiff4-dev
sudo apt install -y libopencv-dev libtesseract-dev
sudo apt install -y zlib1g-dev
sudo apt install -y cmake
sudo apt install -y git
sudo apt install -y build-essential
sudo apt install -y libleptonica-dev
sudo apt install -y liblog4cplus-dev
sudo apt install -y libcurl3-dev
sudo apt install -y imagemagick

sudo apt -y autoremove # for cleanup

if [[ ! -d ~/tesseract-build ]]; then
  echo "$HOME/tesseract-build doesn't exists"
  mkdir tesseract-build
fi

## Configure Leptonica
if [[ ! -d ~/tesseract-build/leptonica-1.79.0 ]]; then
  cd tesseract-build || exit
  echo "$HOME/tesseract-build/leptonica-1.79.0 doesn't exists"
  wget http://www.leptonica.org/source/leptonica-1.79.0.tar.gz
  tar -zxf leptonica-1.79.0.tar.gz && rm -rf leptonica-1.79.0.tar.gz
  cd leptonica-1.79.0 || exit
  ./autobuild
  ./configure
  make
  sudo make install
  sudo ldconfig
fi

## Configure Tesseract
if [[ ! -d ~/tesseract-build/tesseract ]]; then
  echo "$HOME/tesseract-build/tesseract doesn't exists"
  cd ~/tesseract-build || exit
  git clone --depth 1 https://github.com/tesseract-ocr/tesseract.git
  cd tesseract || exit
  ./autogen.sh
  ./configure
  make
  sudo make install
  sudo ldconfig
fi

## Configure TESSDATA
if [[ ! -f ~/tesseract-build/eng.traineddata ]]; then
  ## If needed all language pack that run the below fragment instead
  #  git clone https://github.com/tesseract-ocr/tessdata.git
  #  TESSDATA_PREFIX="/usr/local/share"
  #  sudo cp -r tessdata/eng.traineddata ${TESSDATA_PREFIX}/tessdata
  echo "$HOME/tesseract-build/eng.traineddata doesn't exists"
  cd ~/tesseract-build || exit
  wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata
  TESSDATA_PREFIX="/usr/local/share/tessdata/"
  sudo cp -r eng.traineddata ${TESSDATA_PREFIX}
fi