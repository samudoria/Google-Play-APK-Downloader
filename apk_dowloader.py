import os
import time
import uiautomator2 as u2
import sys


def connect_device():
    device = u2.connect()
    if not device:
        raise RuntimeError(
            "No device connected. Ensure adb is running and the device is connected."
        )
    return device


def open_play_store_and_download(device, package_name):
    play_store_url = (
        f"https://play.google.com/store/apps/details?id={package_name}"
    )
    device.shell(f"am start -a android.intent.action.VIEW -d {play_store_url}")
    time.sleep(5)  # adjust if needed

    if device(text="Install").exists:
        device(text="Install").click()
        print(f"Installing {package_name}...")
    else:
        print(
            f"Install button not found for {package_name}. It might already be installed."
        )
        return False

    while not device(text="Open").exists:
        time.sleep(5)
    print(f"{package_name} installed successfully.")
    return True


def pull_apk(device, package_name, output_dir):
    result = device.shell(f"pm path {package_name}")[0]
    if "package:" not in result:
        print(f"Failed to find APK for {package_name}.")
        return False

    apks = result.split("package:")

    os.makedirs(output_dir, exist_ok=True)
    apk_output_dir = os.path.join(output_dir, package_name)
    os.makedirs(apk_output_dir, exist_ok=True)
    
    for apk_path in apks:
        apk_path = apk_path.strip()
        if apk_path:
            print(f"APK path for {package_name}: {apk_path}")

            os.system(f"adb pull {apk_path} {apk_output_dir}")
            print(f"APK for {package_name} pulled to {apk_output_dir}.")
    return True


def main(package_names, output_dir="apks"):
    device = connect_device()

    for package_name in package_names:
        print(f"Processing {package_name}...")
        if open_play_store_and_download(device, package_name):
            time.sleep(10)
            pull_apk(device, package_name, output_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python downloader.py <path_to_package_names_file> <output_dir>")
        sys.exit(1)

    package_names_file = sys.argv[1]
    output_dir = sys.argv[2]

    with open(package_names_file, "r") as file:
        package_names = [line.strip() for line in file if line.strip()]
    main(package_names, output_dir)
