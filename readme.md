# Huffman encoder-decoder

This is a experiment using Huffman trees to create an "encryption" android app for passing around secret messages to your friends.

![Demo](https://github.com/btonasse/HuffEncoderDecoder/blob/master/desktop/demo/demo.gif)

Do _NOT_ consider this a serious data protection tool. It is merely part of a fun project that I created to play around with Huffman coding.

# Deploying

Source: https://www.youtube.com/watch?v=pzsvN3fuBA0

# Install buildozer

Note: clone the buildozer repo on your repos folder

```shell
git clone https://github.com/kivy/buildozer.git

cd buildozer

sudo python3 setup.py install
```

# Install dependencies

```shell
sudo apt-get update
# sudo apt-get install openjdk-8-jdk # might not be necessary
sudo apt install python3.9-distutils
# sudo apt install cython # Commented out because doesn't work and doesn't seem to be needed
# sudo apt install build-essential libltdl-dev libffi-dev libssl-dev python-dev-is-python3
pip3 install --user --upgrade Cython==0.29.33
sudo apt-get install zip
sudo apt install zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev ipython3
```

# Build and deploy the APK

```shell
buildozer android debug
```

If you want to delete an existing build first, add the `clean` argument

If you want to deploy onto an already connected phone, add the `deploy` argument. You can also make it run right away with `run`. Add `logcat` to get logging.

# Phone config

-   Enable developer options: Settings > About > look for build number and tap 7 times
-   Go to Dev Options and enable:
    -   Stay awake
    -   Enable USB debugging (accept the prompts on the phone)

# Connect to phone with adb

```shell
adb tcpip 5555
```

Click allow again on the phone

Look for your phone's local ip address (About phone > Status)

```shell
adb connect [IP]:5555
```

# Deploy APK

```shell
adb devices

adb -s [DEVICEID] install [NAME_OF_APK_FILE]
```

If installation fails due to `NO_MATCHING_ABIS`, you might need to check which architecture the phone uses and change `buildozer.spec` accordingly. After any changes to the spec, you need to run `buildozer appclean` and rebuild.

The line below in the spec can build multiple architectures and then you can choose:

`android.archs = arm64-v8a, armeabi-v7a`

# Debugging

```shell
adb -s DEVICE_ID logcat *:S python:D
```
