# Google-Play-APK-Downloader
Plug in your favourite device or emulator, enable adb and provide the list of package names.

## Requirements

- Device with debugging enabled
- ADB 
- Install requirements `pip install -r requirements.txt`

## Usage

```
python apk_downloader.py <package_names_file> <output_dir>[OPTIONAL]
```

Provide the path to a text file listing the package names of the apps you would like to download.

The output_dir defaults to './apks' but can be customized.
