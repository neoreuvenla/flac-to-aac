<div align="center">

<br>

<style>
    .scaled-image {
        width: 45%;
        height: auto;
    }
</style>
<img src="img/header.jpg" alt="Logo" class="scaled-image" />

<br>

# FLAC to AAC Converter</div>

This utility allows users to convert FLAC (Free Lossless Audio Codec) files to AAC (Advanced Audio Codec) format. It's specifically tailored for those who want to preserve the rich quality of FLAC files but need the compatibility and smaller file sizes of AAC for mobile music playback. This converter recursively searches the specified directory, locates all FLAC files, and converts them into AAC format at a 256 kbps bit rate. All directory structures, metadata, and album art will be preserved during the conversion.

## Features

- **Batch Conversion**: Convert an entire directory of FLAC files in one go.
- **Parallel Processing**: Uses concurrent processing for faster conversion.
- **Error Logging**: Logs errors and skips files that have already been converted.
- **Interactive CLI**: Simple and interactive command-line interface.

## Prerequisites

You will need to have `ffmpeg` installed on your machine. If you don't have it yet, you can install it using:

    sudo apt-get install ffmpeg

Or follow the official ffmpeg installation guide.

## Usage

* Clone the repository:

        git clone <repository-url>
        cd <repository-directory>

* Run the converter:

        python3 converter.py

Follow the on-screen instructions. You will be prompted to enter the source and destination directories.

## Code Structure

* convert_flac_to_aac_direct(src_file, dest_file): Converts a single FLAC file to AAC.
    
* convert_file_wrapper(args): Wrapper function for parallel processing.
   
* convert_flac_to_aac(src_folder, dest_folder): Recursively searches the source directory for FLAC files and converts them to AAC in the destination directory.

## Logging

* The script logs its actions, especially errors, to a file named conversion.log. This log file is useful for diagnosing failed conversions and understanding the script's actions.

## Limitations

* This utility only supports converting from FLAC to AAC. Other formats are not supported.

* The bitrate for AAC is set at 256 kbps. Adjusting this requires modifying the source code.