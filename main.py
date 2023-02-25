import os
import sys
import subprocess
import tempfile

def get_seven_zip_path():
    seven_zip_executable = "7z"
    seven_zip_path = None
    
    if os.name == "nt":
        for path in os.environ["PATH"].split(os.pathsep):
            exe_path = os.path.join(path, seven_zip_executable + ".exe")
            if os.path.exists(exe_path):
                seven_zip_path = exe_path
                break
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_path = os.path.join(path, seven_zip_executable)
            if os.path.exists(exe_path):
                seven_zip_path = exe_path
                break
        if not seven_zip_path:
            default_paths = [
                "/usr/local/bin/{}".format(seven_zip_executable),
                "/usr/bin/{}".format(seven_zip_executable),
                "/usr/local/{}".format(seven_zip_executable)
            ]
            for path in default_paths:
                if os.path.exists(path):
                    seven_zip_path = path
                    break

    return seven_zip_path

def main():
    # Search for 7zip executable
    seven_zip = get_seven_zip_path()

    if not seven_zip:
        print("Error: 7zip is not installed!")
        sys.exit(1)

    # Get the path of the dragged file
    path = sys.argv[1]

    if not os.path.exists(path):
        print("Error: File does not exist!")

    # Get the extension of the dragged file
    extension = os.path.splitext(path)[1]

    # Get the directory path of the dragged file
    dir_path = os.path.dirname(path)

    # Get the base filename of the dragged file without extension
    base_filename = os.path.splitext(os.path.basename(path))[0]

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Extract the compressed file to the temporary directory
        subprocess.call([seven_zip, "x", "-y", "-o" + tmp_dir, path])

        # Create the output zip file path
        zip_file_path = os.path.join(dir_path, base_filename + ".zip")

        # Compress the contents of the temporary directory into a zip archive
        subprocess.call([seven_zip, "a", "-m0=lzma", "-r", "-tzip", zip_file_path, f"{tmp_dir}/*"])
    print("File converted to zip archive: ", zip_file_path)

if __name__ == '__main__':
    main()
