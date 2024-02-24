### demucs binary


Create a docker image with demucs binary

```bash
git clone https://github.com/SadeghKrmi/demucs.git
cd demucs
docker image build -it demucs:v1 .
```

Run the container using demucs:v1 image and bind a directory with input audios

```bash
docker container run -it --name demucs -v /root/audio-in/:/app/audio-in demucs:v1 bash
```


In `Dockerfile` pyinstaller is used to generate binary executables for demucs
First time creating the .spec file, not recommended for this repo

```bash
cd /app/app 
pyinstaller --add-data="/usr/local/lib/python3.11/site-packages/demucs:demucs/" separator.py --onefile
```

Running using .spec file contianing the spec to exclude un-used packages, etc.
Excluding the nvidia cuda python packages, to create lower image size running only over `CPU`

```bash
pyinstaller separator.spec
```
