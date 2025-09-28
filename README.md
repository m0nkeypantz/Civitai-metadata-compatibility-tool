# AI Image Metadata Tool for Civitai

A simple Python GUI application that adds AI generation metadata to images, allowing them to be uploaded to Civitai without metadata detection errors.

## Problem Solved

When uploading images to Civitai, the platform requires AI generation metadata to be present in the image files. Without this metadata, uploads are blocked with "can't detect metadata" errors. This tool adds realistic AI generation metadata to your images, making them compatible with Civitai's requirements.

## Features

- **Drag & Drop Interface**: Simply drag and drop your images into the application
- **Realistic AI Metadata**: Generates authentic-looking AI generation parameters including:
  - Prompts and negative prompts
  - Model information (Realistic Vision XL, DreamShaper XL, etc.)
  - Generation parameters (steps, sampler, CFG scale, seed, etc.)
  - LoRA and embedding information
  - Civitai resource references
- **Custom Prompts**: Option to use your own custom prompts
- **Batch Processing**: Process multiple images at once
- **Safe Processing**: Creates new files with `_with_metadata` suffix, preserving originals

## Installation

1. **Install Python** (if not already installed):
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python ai_image_metadata_tool.py
   ```

## Usage

1. **Launch the Application**:
   - Run `python ai_image_metadata_tool.py`
   - The GUI window will open

2. **Add Images**:
   - **Method 1**: Drag and drop image files directly into the drop area
   - **Method 2**: Click "Select Images" button to browse for files
   - Supported formats: JPG, JPEG, PNG

3. **Configure Options**:
   - **Random Parameters**: Keep checked for automatic random generation parameters
   - **Custom Prompt**: Check this and enter your own prompt if desired

4. **Process Images**:
   - Click "Add AI Metadata" button
   - Watch the progress in the status area
   - New files will be created with `_with_metadata` suffix

5. **Upload to Civitai**:
   - Use the new files (with `_with_metadata` suffix) for Civitai uploads
   - The metadata detection error should be resolved

## Generated Metadata Format

The tool generates metadata in the exact format Civitai expects, stored in the image's "User Comment" EXIF field:

```
masterpiece, best quality, highly detailed, beautiful woman, portrait, elegant dress, soft lighting, professional photographyNegative prompt: low quality, blurry, pixelated, jpeg artifacts, worst quality, bad anatomySteps: 35, Sampler: Euler a, CFG scale: 7.5, Seed: 1234567890, Size: 1024x1024, Clip skip: 2, Created Date: 2024-09-25T15:30:00.000000Z, Civitai resources: [{"type":"checkpoint","modelVersionId":130072,"modelName":"Realistic Vision XL","modelVersionName":"v6.0 (BakedVAE)"}]
```

## Included AI Models & Resources

The tool randomly selects from a curated list of popular AI models and resources:

### Models
- Realistic Vision XL
- DreamShaper XL  
- SDXL Base
- Juggernaut XL
- RealitiesEdge XL
- Anime Art Diffusion XL
- Crystal Clear XL

### LoRAs
- Detail Tweaker XL
- xl_more_art-full
- Skin Detail XL
- Eye Enhancement XL
- Background Enhancer

### Samplers
- Euler a, Euler, DPM++ 2M, DPM++ SDE, DPM++ 2M Karras, etc.

## Troubleshooting

### "Module not found" errors
- Make sure you installed the requirements: `pip install -r requirements.txt`
- Try using `pip3` instead of `pip` if on Mac/Linux

### "Permission denied" errors
- Make sure you have write permissions in the folder containing your images
- Try running as administrator (Windows) or with `sudo` (Mac/Linux)

### Images still rejected by Civitai
- Make sure you're uploading the files with `_with_metadata` suffix
- Try processing the images again with different random parameters
- Check that the original images are in supported formats (JPG, PNG)

## Technical Details

- **Language**: Python 3.7+
- **GUI Framework**: Tkinter with tkinterdnd2 for drag & drop
- **Image Processing**: Pillow (PIL) for image handling
- **Metadata**: piexif for EXIF data manipulation
- **Format**: Follows Civitai's exact metadata format specification

## File Structure

```
MetaData/
├── ai_image_metadata_tool.py  # Main application
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## License

This tool is provided as-is for educational and personal use. Feel free to modify and distribute as needed.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Make sure all dependencies are installed correctly
3. Verify your Python version is 3.7 or higher
4. Check that your images are in supported formats

## Version History

- **v1.0**: Initial release with drag & drop interface and AI metadata generation
