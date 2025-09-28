#!/usr/bin/env python3
"""
Simple AI Image Metadata Tool for Civitai (No Drag & Drop)
A simple GUI application to add AI generation metadata to images for Civitai uploads.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import random
from PIL import Image
import piexif
import json
from datetime import datetime, timedelta

class SimpleAIImageMetadataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple AI Image Metadata Tool for Civitai")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f0f0')
        
        # AI Generation metadata pools
        self.prompts = [
            "masterpiece, best quality, highly detailed, beautiful woman, portrait, elegant dress, soft lighting, professional photography",
            "anime style, cute girl, colorful hair, fantasy background, magical atmosphere, detailed eyes, vibrant colors",
            "realistic portrait, handsome man, professional suit, studio lighting, sharp focus, high resolution",
            "landscape, mountain vista, sunset, dramatic clouds, cinematic lighting, photorealistic, 8k resolution",
            "fantasy art, dragon, medieval castle, epic scene, detailed armor, magical effects, concept art style",
            "cyberpunk cityscape, neon lights, futuristic buildings, rain effects, moody atmosphere, sci-fi",
            "oil painting style, classical portrait, renaissance art, detailed brushwork, warm colors, artistic",
            "digital art, space scene, nebula, stars, cosmic colors, ethereal lighting, science fiction"
        ]
        
        self.negative_prompts = [
            "low quality, blurry, pixelated, jpeg artifacts, worst quality, bad anatomy",
            "ugly, deformed, disfigured, mutation, extra limbs, bad proportions, watermark",
            "text, signature, username, error, cropped, out of frame, lowres, normal quality",
            "bad hands, missing fingers, extra fingers, poorly drawn hands, malformed limbs",
            "duplicate, morbid, mutilated, poorly drawn face, bad art, gross proportions"
        ]
        
        self.models = [
            {"name": "Realistic Vision XL", "version": "v6.0 (BakedVAE)", "id": 130072},
            {"name": "DreamShaper XL", "version": "v2.1 Turbo", "id": 112902},
            {"name": "SDXL Base", "version": "v1.0", "id": 101055},
            {"name": "Juggernaut XL", "version": "v9 + RunDiffusion", "id": 288982},
            {"name": "RealitiesEdge XL", "version": "v7 (BakedVAE)", "id": 346399},
            {"name": "Anime Art Diffusion XL", "version": "v3.1", "id": 117259},
            {"name": "Crystal Clear XL", "version": "v1.0", "id": 137116}
        ]
        
        self.loras = [
            {"name": "Detail Tweaker XL", "version": "v1.0", "id": 122359, "weight": 0.8},
            {"name": "xl_more_art-full", "version": "v1", "id": 152309, "weight": 0.75},
            {"name": "Skin Detail XL", "version": "v1.2", "id": 156927, "weight": 0.6},
            {"name": "Eye Enhancement XL", "version": "v1.0", "id": 143906, "weight": 0.5},
            {"name": "Background Enhancer", "version": "v2.0", "id": 167832, "weight": 0.7}
        ]
        
        self.embeddings = [
            {"name": "Civitai Safe Helper", "version": "v1.0", "id": 106916},
            {"name": "BadDream", "version": "v1.0", "id": 77169},
            {"name": "UnrealisticDream", "version": "v1.0", "id": 77173}
        ]
        
        self.samplers = [
            "Euler a", "Euler", "DPM++ 2M", "DPM++ SDE", "DPM++ 2M Karras", 
            "DPM++ SDE Karras", "DDIM", "PLMS", "UniPC", "DPM2 a Karras"
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Simple AI Image Metadata Tool for Civitai", 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Click 'Select Images' to choose your images and add AI generation metadata",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        instructions.pack(pady=5)
        
        # File selection area
        self.file_frame = tk.Frame(
            self.root, 
            width=500, 
            height=100, 
            bg='#ffffff',
            relief='ridge',
            bd=2
        )
        self.file_frame.pack(pady=20, padx=20, fill='x')
        self.file_frame.pack_propagate(False)
        
        # File area label
        self.file_label = tk.Label(
            self.file_frame,
            text="🖼️\n\nNo images selected\n\nClick 'Select Images' below",
            font=("Arial", 12),
            bg='#ffffff',
            fg='#999999'
        )
        self.file_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Options frame
        options_frame = tk.LabelFrame(self.root, text="Generation Options", bg='#f0f0f0', font=("Arial", 10, "bold"))
        options_frame.pack(pady=10, padx=20, fill='x')
        
        # Randomization options
        self.random_var = tk.BooleanVar(value=True)
        random_check = tk.Checkbutton(
            options_frame, 
            text="Use random generation parameters", 
            variable=self.random_var,
            bg='#f0f0f0',
            font=("Arial", 9)
        )
        random_check.pack(anchor='w', padx=10, pady=5)
        
        # Custom prompt option
        self.custom_prompt_var = tk.BooleanVar(value=False)
        custom_check = tk.Checkbutton(
            options_frame, 
            text="Use custom prompt (leave empty for random)", 
            variable=self.custom_prompt_var,
            bg='#f0f0f0',
            font=("Arial", 9)
        )
        custom_check.pack(anchor='w', padx=10, pady=2)
        
        # Custom prompt entry
        self.custom_prompt_entry = tk.Text(options_frame, height=3, width=60, font=("Arial", 9))
        self.custom_prompt_entry.pack(padx=10, pady=5, fill='x')
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # Select files button
        select_btn = tk.Button(
            button_frame,
            text="Select Images",
            command=self.select_files,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=30,
            pady=15,
            relief='flat'
        )
        select_btn.pack(side='left', padx=10)
        
        # Process button
        self.process_btn = tk.Button(
            button_frame,
            text="Add AI Metadata",
            command=self.process_images,
            bg='#2196F3',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=30,
            pady=15,
            relief='flat',
            state='disabled'
        )
        self.process_btn.pack(side='left', padx=10)
        
        # Status area
        self.status_text = tk.Text(
            self.root,
            height=12,
            width=70,
            bg='#f9f9f9',
            fg='#333333',
            font=("Consolas", 9),
            wrap='word'
        )
        self.status_text.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Scrollbar for status text
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side='right', fill='y')
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        self.selected_files = []
        self.log_message("Application started successfully!")
        self.log_message("Select your PNG/JPG images to add AI metadata for Civitai upload")
        
    def log_message(self, message):
        """Add a message to the status text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()
            
    def select_files(self):
        """Open file dialog to select images"""
        files = filedialog.askopenfilenames(
            title="Select AI Images",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            self.selected_files = list(files)
            self.log_message(f"Selected {len(files)} image(s):")
            for file in files:
                self.log_message(f"  - {os.path.basename(file)}")
            
            # Update the file area display
            if len(files) == 1:
                self.file_label.config(text=f"🖼️\n\n1 image selected:\n{os.path.basename(files[0])}")
            else:
                self.file_label.config(text=f"🖼️\n\n{len(files)} images selected\n\nReady to process!")
            
            self.process_btn.config(state='normal')
            
    def generate_ai_metadata(self):
        """Generate random AI generation metadata in Civitai format"""
        # Get custom prompt if specified
        if self.custom_prompt_var.get():
            custom_prompt = self.custom_prompt_entry.get("1.0", tk.END).strip()
            prompt = custom_prompt if custom_prompt else random.choice(self.prompts)
        else:
            prompt = random.choice(self.prompts)
            
        negative_prompt = random.choice(self.negative_prompts)
        
        # Random generation parameters
        steps = random.randint(20, 50)
        sampler = random.choice(self.samplers)
        cfg_scale = round(random.uniform(4.0, 12.0), 1)
        seed = random.randint(1000000, 9999999999)
        
        # Random image dimensions (common AI image sizes)
        sizes = ["512x512", "768x768", "1024x1024", "512x768", "768x512", "1216x832", "832x1216"]
        size = random.choice(sizes)
        
        clip_skip = random.randint(1, 2)
        
        # Random date within last year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        created_date = random_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Select random model and resources
        model = random.choice(self.models)
        selected_loras = random.sample(self.loras, random.randint(0, 2))
        selected_embeddings = random.sample(self.embeddings, random.randint(0, 1))
        
        # Build Civitai resources array
        resources = []
        
        # Add main model
        resources.append({
            "type": "checkpoint",
            "modelVersionId": model["id"],
            "modelName": model["name"],
            "modelVersionName": model["version"]
        })
        
        # Add LoRAs
        for lora in selected_loras:
            resources.append({
                "type": "lora",
                "weight": lora["weight"],
                "modelVersionId": lora["id"],
                "modelName": lora["name"],
                "modelVersionName": lora["version"]
            })
            
        # Add embeddings
        for embed in selected_embeddings:
            resources.append({
                "type": "embed",
                "modelVersionId": embed["id"],
                "modelName": embed["name"],
                "modelVersionName": embed["version"]
            })
        
        # Format the metadata string exactly like Civitai expects
        metadata_string = f"{prompt}Negative prompt: {negative_prompt}Steps: {steps}, Sampler: {sampler}, CFG scale: {cfg_scale}, Seed: {seed}, Size: {size}, Clip skip: {clip_skip}, Created Date: {created_date}, Civitai resources: {json.dumps(resources, separators=(',', ':'))}"
        
        return metadata_string
        
    def add_ai_metadata_to_image(self, image_path, metadata_string):
        """Add AI generation metadata to an image file"""
        try:
            self.log_message(f"Processing: {os.path.basename(image_path)}")
            
            # Open the image
            image = Image.open(image_path)
            
            # Get existing EXIF data or create new
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            if "exif" in image.info:
                exif_dict = piexif.load(image.info["exif"])
            
            # Add the AI metadata to User Comment field
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = "AI Generated Image"
            
            # Handle different piexif versions
            try:
                # Try the newer method first
                user_comment = metadata_string.encode('utf-8')
                # Add the encoding prefix for UserComment
                user_comment = b'UNICODE\x00' + user_comment
                exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment
            except Exception as e:
                # Fallback to older method if available
                try:
                    exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(metadata_string, encoding="unicode")
                except:
                    # If both fail, just encode as UTF-8
                    exif_dict["Exif"][piexif.ExifIFD.UserComment] = metadata_string.encode('utf-8')
            
            # Add software info
            exif_dict["0th"][piexif.ImageIFD.Software] = "AI Image Generator"
            
            # Convert back to bytes
            exif_bytes = piexif.dump(exif_dict)
            
            # Create output filename
            base_name = os.path.splitext(image_path)[0]
            ext = os.path.splitext(image_path)[1]
            output_path = f"{base_name}_with_metadata{ext}"
            
            # Save with metadata
            if image.mode == 'RGBA':
                # Convert RGBA to RGB for JPEG compatibility
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[-1])
                rgb_image.save(output_path, exif=exif_bytes, quality=95)
            else:
                image.save(output_path, exif=exif_bytes, quality=95)
            
            return output_path, True, None
            
        except Exception as e:
            return None, False, str(e)
            
    def process_images(self):
        """Process all selected images and add AI metadata"""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select some images first")
            return
            
        self.log_message(f"\n🚀 Starting to process {len(self.selected_files)} image(s)...")
        
        success_count = 0
        error_count = 0
        
        for i, image_path in enumerate(self.selected_files):
            self.log_message(f"\n--- Processing {i+1}/{len(self.selected_files)} ---")
            
            # Generate AI metadata
            metadata_string = self.generate_ai_metadata()
            
            # Add metadata to image
            output_path, success, error = self.add_ai_metadata_to_image(image_path, metadata_string)
            
            if success:
                success_count += 1
                self.log_message(f"✅ Success: {os.path.basename(output_path)}")
                # Show a preview of the metadata
                preview = metadata_string[:150] + "..." if len(metadata_string) > 150 else metadata_string
                self.log_message(f"   Metadata: {preview}")
            else:
                error_count += 1
                self.log_message(f"❌ Error: {error}")
        
        # Final summary
        self.log_message(f"\n🎉 Processing complete!")
        self.log_message(f"✅ Successfully processed: {success_count}")
        if error_count > 0:
            self.log_message(f"❌ Errors: {error_count}")
        
        self.log_message(f"\n📁 Images with AI metadata are saved with '_with_metadata' suffix.")
        self.log_message(f"🚀 You can now upload these images to Civitai!")
        
        messagebox.showinfo(
            "Processing Complete", 
            f"Successfully processed {success_count} image(s).\n"
            f"Files saved with '_with_metadata' suffix.\n"
            f"Ready for Civitai upload!"
        )

def main():
    # Create the main window
    root = tk.Tk()
    app = SimpleAIImageMetadataApp(root)
    
    # Add some styling
    style = ttk.Style()
    style.theme_use('clam')
    
    root.mainloop()

if __name__ == "__main__":
    main()
