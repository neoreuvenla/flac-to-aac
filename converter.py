from concurrent.futures import ProcessPoolExecutor
import logging
import os
from PIL import Image
import subprocess
from tqdm import tqdm

# convert flac to aac
def flac_conversion(src_file, dest_file):

    # extract artwork to current folder
    dest_dir = os.path.dirname(dest_file)
    extract_artwork(src_file, dest_dir)
    
    command = [ 
        # encoding settings
        'ffmpeg',        # executable utility
        '-i', src_file,  # input file
        '-vn',           # exclude artwork from conversion
        '-ar', '44100',  # set sample rate to 44100 Hz
        '-c:a', 'aac',   # encoding format
        '-b:a', '256k',  # audio bitrate in kbps
        
        # metadata removal
        '-metadata', 'album_artist=',
        '-metadata', 'genre=',
        '-metadata', 'comment=',
        '-metadata', 'composer=',
        '-metadata', 'original_artist=',
        '-metadata', 'copyright=',
        '-metadata', 'url=',
        '-metadata', 'encoded_by=',
        '-metadata', 'lyrics=',
        
        # file output
        dest_file]

    try:
        # spawn new process to run the command
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        # unsuccessful conversion log message
        logging.error(f"Failed to convert {src_file}: {e}")
        print(f"\nFailed to convert {src_file}")

# wrapper function to facilitate parallel processing
def conversion_wrapper(args):
    return flac_conversion(*args)

# extract flac artwork
def extract_artwork(src_file, dest_dir):

    # album artwork full path
    art_file = os.path.join(dest_dir, 'cover.jpg')
    
    command = [
        # artwork extraction
        'metaflac',                         # executable utility
        '--export-picture-to=' + art_file,  # extract artwork to path
        
        # file input
        src_file]

    try:
        # spawn new process to run the command with a timeout
        subprocess.run(command, check=True, timeout=10)
        
        # resize the output
        resize_image(art_file, (200, 200))

    except subprocess.CalledProcessError as e:
        # unsuccessful extraction log message
        logging.warning(f"Failed to extract album art from {src_file}: {e}")
        print(f"\nFailed to extract album art from {src_file}")

    except subprocess.TimeoutExpired:
        # timeout log message
        logging.warning(f"Timeout occured while extracting album art from {src_file}")
        print(f"\nTimeout occured while extracting album art from {src_file}")

# resize jpeg image
def resize_image(image_path, new_size):

    try:
        # resize the image
        with Image.open(image_path) as img:
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            img.save(image_path, "JPEG")
    
    except OSError as e:
        if "image file is truncated" in str(e):
            # corrupted image log message
            logging.warning(f"Corrupted image file detected: {image_path}")
        else:
            # resize error log message
            logging.error(f"Error processing image {image_path}: {e}")

# check leafs for missing artwork 
def artwork_missing(root_folder):
    
    # check for artwork in leaf folders 
    folders_missing = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
       
        # check if folder is a leaf
        if not dirnames:
           
            # add path to list if no image found
            if 'cover.jpg' not in filenames:
                folders_missing.append(dirpath)

    return folders_missing

# coordinate parallel conversions 
def conversion_coordination(src_folder, dest_folder):

    # create destination folder if needed
    if not os.path.exists(dest_folder):
        try:
            os.makedirs(dest_folder)
        except Exception as e:
            logging.error(f"Failed to create directory {dest_folder}: {e}")
            print(f"Error: Failed to create directory {dest_folder}")
            return

    # check destination folder is writeable
    if not os.access(dest_folder, os.W_OK):
        logging.error(f"Destination folder {dest_folder} is not writable")
        print(f"Error: Destination folder {dest_folder} is not writable")
        return

    # list all flac paths in source folder
    flac_files = []
    for dirpath, _, filenames in os.walk(src_folder):
        for filename in filenames:
            if filename.endswith('.flac'):
                flac_files.append(os.path.join(dirpath, filename))

    # list source and destination paths
    args_list = []
    for src_file in flac_files:

        rel_path = os.path.relpath(src_file, src_folder)
        dest_file = os.path.join(dest_folder, rel_path.replace('.flac', '.m4a'))

        # skip if destination path structure already exists
        if os.path.exists(dest_file):
            continue

        # check specific folder exists before file conversion
        dest_dir = os.path.dirname(dest_file)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
                logging.error(f"Failed to create directory {dest_dir}: {e}")
                continue

        # append source and destination paths
        args_list.append((src_file, dest_file))

    # convert flacs in parallel
    with ProcessPoolExecutor() as executor:
        list(tqdm(                                        #  provides progress bar
            executor.map(conversion_wrapper, args_list),  #  executed function and arguments
            total=len(args_list),                         #  total task count 
            unit="file"))                                 #  task unit

# log info warning error and critical messages
logging.basicConfig(filename="conversion.log", 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# main execution code
if __name__ == "__main__":

    # header text block
    print("\n")
    print("+" + "-"*80 + "+")
    print("|" + " "*80 + "|")
    print("|" + "     ;;;;;;;;;;;;;;;;;;;".center(80) + "|")
    print("|" + "     ;;;;;;;;;;;;;;;;;;;".center(80) + "|")
    print("|" + "     ;                 ;".center(80) + "|")
    print("|" + "     ;                 ;".center(80) + "|")
    print("|" + "     ;                 ;".center(80) + "|")
    print("|" + "     ;                 ;".center(80) + "|")
    print("|" + "     ;                 ;".center(80) + "|")
    print("|" + "     ;                 ;".center(80) + "|")
    print("|" + ",;;;;;            ,;;;;;".center(80) + "|")
    print("|" + ";;;;;;            ;;;;;;".center(80) + "|")
    print("|" + "`;;;;'            `;;;;'".center(80) + "|")
    print("|" + " "*80 + "|")
    print("|" + "FLAC / AAC CONVERTER".center(80) + "|")
    print("|" + " "*80 + "|")
    print("+" + "-"*80 + "+")
    print("|" + "Convert lossless FLAC files into lossy AAC files for portable playback".center(80) + "|")
    print("|" + "Refer to github.com/neoreuvenla/flac-to-aac for more information".center(80) + "|")
    print("+" + "-"*80 + "+")
    
    while True:
        # user input block
        print("\n")
        src_folder = input("| Enter source path, eg ~/Music/FLAC:\t  ")
        dest_folder = input("| Enter destination path, eg ~/Music/AAC: ")
        print("\n")

        # expand home directory to full path 
        src_folder = os.path.expanduser(src_folder)
        dest_folder = os.path.expanduser(dest_folder)

        
        if os.path.isdir(src_folder):
            # break loop if source is valid
            break 

        else:
            # reprompt if source is invalid
            print(f"| '{src_folder}' is not a valid directory")

    # start conversion
    conversion_coordination(src_folder, dest_folder)

    # album artwork extraction check
    missing_covers = artwork_missing(dest_folder)
    
    if missing_covers:
        # missing artwork detected
        print("\nCheck log for folders missing artwork")

        for folder in missing_covers:
            # artwork missing log message
            logging.info(f"Missing artwork: {folder}")