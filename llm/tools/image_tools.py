import tempfile
import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes


class ImageTools:
    """
    ImageTools class provides methods to handle image processing tasks required for VQA operations.
    """

    def __init__(self):
        """
        Initialize the ImageTools class.
        """
        self.log = st.logger.get_logger(__name__)
        self.log.debug("ImageTools initialized")

    def pdf_to_jpeg(self, byte_obj, dpi=200):
        """
        Convert PDF file to a JPEG image. Multiple pages are converted to individual images
        and then merged.
        Args:
            uploaded_file (UploadedFile): PDF file uploaded by the user via Streamlit file uploader.
            byte_obj (bytes): Byte object of the PDF file.
            dpi (int): Dots per inch for the conversion. Default is 200.
        Returns:
            image_bytes: byte object containing all image data.
        """
        jpeg_image_path = image_byte_data = None
        try:
            # Convert to PIL image list
            images = convert_from_bytes(byte_obj, dpi=dpi, fmt='jpeg')    
            image_count = len(images)
            if image_count>1:
                jpeg_image_path = self._merge_images(images)
            else:
                image = images[0].convert("RGB")
                image = image.resize((1024, 1024))  # Llama Vision: max size is 1120x1120
                self.log.debug(f"image size: {image.size}")
                jpeg_image_path = self.get_temp_jpeg(image)

            with open(jpeg_image_path, 'rb') as file:
                image_byte_data = file.read()      
        
        except FileNotFoundError as ferr:
            self.log.critical(f"FileNotFoundError {jpeg_image_path}: {ferr}")
            raise FileNotFoundError("Failed to read coverted JPEG image! Please check the file path or permissions and try again.")
        except Exception as err:
            self.log.critical(f"{type(err)}: Error converting PDF to image: {err}")
            raise RuntimeError("Failed to convert the PDF document to JPEG image. Please investigate the file format and content for corruption.")

        return image_byte_data

    def _merge_images(self, images):
        """
        Merge multiple images into a single one. Logic scales merged image to maintain 
        aspect ratio and attempt fit within max constraints of Llama Vision.  Overall results 
        depreciate with image size. Llama Vision context window is 128k tokens and data truncates.
        Args:
            images (list): List of PIL Image objects to merge.
        Returns:
            PIL Image: Merged image.
        """
        tmp_image_paths = []
        merged_image_name = "merged_pages.jpeg"
        for index, image in enumerate(images):
            self.log.debug(f"Converting page {index + 1} of PDF to image")
            image.convert("RGB")
            jpeg_path = self.get_temp_jpeg(image)
            tmp_image_paths.append(jpeg_path)
    
        self.log.debug(f"Total pages converted: {len(tmp_image_paths)}")
        imgs = list(map(Image.open, tmp_image_paths))
        # Find max width, ttl height of images
        max_img_width = max(i.width for i in imgs)
        total_height = sum(i.height for i in imgs)
    
        # New image for merged pages
        merged_image = Image.new('RGB', (max_img_width, total_height))
        y_offset = 0
        for img in imgs:
            merged_image.paste(img, (0, y_offset))   # Merge images
            y_offset += img.height                   # Reset y_offset for vertical stacking

        img_width, img_height = merged_image.size
        new_height = int((1024 / img_width) * img_height)  # Scale to maintain aspect ratio
        merged_image = merged_image.resize((1024, new_height))  # Llama Vision: max size is 1120x1120               
        self.log.debug(f"Merged image size: {merged_image.size}")
        merged_image_path = self.get_temp_jpeg(merged_image) 
        return merged_image_path
    
    def get_temp_jpeg(self, image):
        """
        Create a temporary JPEG file.
        Returns:
            str: Path to the temporary JPEG file.
        """
        jpeg_path = None
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg") as tmp_file:
            image.save(tmp_file, "JPEG")
            jpeg_path = tmp_file.name
            self.log.debug(f"Saved image as {jpeg_path}")  
        return jpeg_path  