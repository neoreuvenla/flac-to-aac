import os
import subprocess
import logging
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

# Set up logging
logging.basicConfig(filename="conversion.log", level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


#def convert_flac_to_aac_direct(src_file, dest_file):
#    command = [
#        'ffmpeg',
#        '-i', src_file,
#        '-vn',  # Exclude video streams
#        '-c:a', 'aac',
#        '-b:a', '256k',
#        dest_file
#    ]
#    try:
#        subprocess.run(command, check=True)
#        logging.info(f"Successfully converted {src_file} to {dest_file}.")
#    except subprocess.CalledProcessError as e:
#        logging.error(f"Failed to convert {src_file}. Reason: {e}")
#        print(f"\nFailed to convert {src_file}. Check the log for details.")

def convert_flac_to_aac_direct(src_file, dest_file):
    command = [
        'ffmpeg',
        '-i', src_file,
        '-vn',  # Exclude video streams
        '-c:a', 'aac',
        '-b:a', '256k',
        
        # Metadata fields to drop
        '-metadata', 'album_artist=',
        '-metadata', 'genre=',
        '-metadata', 'comment=',
        '-metadata', 'composer=',
        '-metadata', 'original_artist=',
        '-metadata', 'copyright=',
        '-metadata', 'url=',
        '-metadata', 'encoded_by=',
        '-metadata', 'lyrics=',
        
        dest_file
    ]
    try:
        subprocess.run(command, check=True)
        logging.info(f"Successfully converted {src_file} to {dest_file}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to convert {src_file}. Reason: {e}")
        print(f"\nFailed to convert {src_file}. Check the log for details.")


def convert_file_wrapper(args):
    return convert_flac_to_aac_direct(*args)


def convert_flac_to_aac(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        try:
            os.makedirs(dest_folder)
        except Exception as e:
            logging.error(f"Failed to create directory {dest_folder}. Reason: {e}")
            print(f"Error: Failed to create directory {dest_folder}. Exiting.")
            return

    # Check if dest_folder is writable
    if not os.access(dest_folder, os.W_OK):
        logging.error(f"Destination folder {dest_folder} is not writable.")
        print(f"Error: Destination folder {dest_folder} is not writable. Exiting.")
        return

    # Collect all FLAC files first to determine total for the progress bar
    flac_files = []
    for dirpath, _, filenames in os.walk(src_folder):
        for filename in filenames:
            if filename.endswith('.flac'):
                flac_files.append(os.path.join(dirpath, filename))

    args_list = []
    for src_file in flac_files:
        rel_path = os.path.relpath(src_file, src_folder)
        dest_file = os.path.join(dest_folder, rel_path.replace('.flac', '.m4a'))

        if os.path.exists(dest_file):
            logging.info(f"Skipping {src_file} as destination file already exists.")
            continue

        dest_dir = os.path.dirname(dest_file)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
                logging.error(f"Failed to create directory {dest_dir}. Reason: {e}")
                continue

        args_list.append((src_file, dest_file))

    # Convert each FLAC file in parallel, updating the progress bar
    with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(convert_file_wrapper, args_list), total=len(args_list), unit="file"))

if __name__ == "__main__":

    # Add some spacing for readability
    print("\n")

    # Use a border for the title
    print("+" + "-"*80 + "+")
    print("|" + "FLAC TO AAC CONVERTER".center(80) + "|")
    print("|" + " "*80 + "|")
    print("|" + "Convert lossless FLAC files into AAC files for mobile music playback".center(80) + "|")
    print("+" + "-"*80 + "+")
    print("|" + "This program will recursively search through the specified directory, locating".center(80) + "|")
    print("|" + "all FLAC files and converting them into the AAC format at a 256 kbps bit rate.".center(80) + "|")
    print("|" + "All directory structures, meta data, and album art will be preserved".center(80) + "|")
    print("+" + "-"*80 + "+")
    
    # Add some spacing for readability
    print("\n")
    
    # Prompt the user for folder paths
    src_folder = input("| Enter source path, eg ~/Music/FLAC:\t  ")
    dest_folder = input("| Enter destination path, eg ~/Music/AAC: ")
    
    # Add some spacing for readability
    print("\n")

    # Expanding the '~' character for both src_folder and dest_folder
    src_folder = os.path.expanduser(src_folder)
    dest_folder = os.path.expanduser(dest_folder)

    # Check if the expanded src_folder is a valid directory
    if not os.path.isdir(src_folder):
        logging.error(f"| '{src_folder}' is not a valid directory.")
        print(f"| '{src_folder}' is not a valid directory. Exiting.")
        exit(1)

    convert_flac_to_aac(src_folder, dest_folder)
