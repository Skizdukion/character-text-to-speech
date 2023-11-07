### Manual installation using Conda

#### 1. Install requirements

```
pip install -r requirements.txt
```

#### 2. Download nltk
```
python -m nltk.downloader punkt
```

#### 3. Install ffmpeg
```
apt install ffmpeg
```

#### 4. Setup bark checkpoint
```
chmod +x setup-bark.sh
./setup-bark.sh
```

#### 5. Run Server
```
cd src
python main.py
```
