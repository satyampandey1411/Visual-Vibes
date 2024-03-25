from flask import Flask, render_template, request
from PIL import Image, ImageEnhance, ImageFilter
import io 
import base64
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('editing.html')

@app.route('/rotate', methods=['POST'])
def rotate():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image selected", 400

    angle = int(request.form['angle'])
    rotated_image_data = rotate_image(image_file, angle)
    
    return rotated_image_data, 200

def rotate_image(image_file, angle):
    image = Image.open(image_file)
    rotated_image = image.rotate(angle, expand=True)
    
    # Convert rotated image to base64 string
    image_buffer = io.BytesIO()
    rotated_image.save(image_buffer, format='PNG')
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    
    return encoded_image

@app.route('/blur', methods=['POST'])
def blur():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image selected", 400

    intensity = int(request.form['intensity'])
    blurred_image_data = blur_image(image_file, intensity)
    
    return blurred_image_data, 200

def blur_image(image_file, intensity):
    image = Image.open(image_file)
    blurred_image = image.filter(ImageFilter.GaussianBlur(intensity))
    
    # Convert blurred image to base64 string
    image_buffer = io.BytesIO()
    blurred_image.save(image_buffer, format='PNG')
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    
    return encoded_image

@app.route('/adjust_contrast', methods=['POST'])
def adjust_contrast():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image selected", 400

    contrast_factor = float(request.form['contrast'])
    adjusted_image_data = adjust_image_contrast(image_file, contrast_factor)
    
    return adjusted_image_data, 200

def adjust_image_contrast(image_file, contrast_factor):
    # Open the image using PIL
    image = Image.open(image_file)
    
    # Create an enhancer object
    enhancer = ImageEnhance.Contrast(image)
    
    # Adjust the contrast
    adjusted_image = enhancer.enhance(contrast_factor)
    
    # Convert the adjusted image to base64 string
    buffered = BytesIO()
    adjusted_image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_image

@app.route('/adjust_brightness', methods=['POST'])
def adjust_brightness():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image selected", 400

    brightness = float(request.form['brightness']) / 100.0
    adjusted_image_data = adjust_brightness(image_file, brightness)
    
    return adjusted_image_data, 200

def adjust_brightness(image_file, brightness):
    image = Image.open(image_file)
    enhancer = ImageEnhance.Brightness(image)
    adjusted_image = enhancer.enhance(brightness)
    
    # Convert adjusted image to base64 string
    image_buffer = io.BytesIO()
    adjusted_image.save(image_buffer, format='PNG')
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    return encoded_image

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image selected", 400

    filter_type = request.form['filter']
    filtered_image_data = apply_filter_to_image(image_file, filter_type)
    
    return filtered_image_data, 200

def apply_filter_to_image(image_file, filter_type):
    image = Image.open(image_file)
    
    if filter_type == 'grayscale':
        filtered_image = image.convert('L')
    elif filter_type == 'fine_edges':
        filtered_image = image.filter(ImageFilter.FIND_EDGES)
    elif filter_type == 'emboss':
        filtered_image = image.filter(ImageFilter.EMBOSS)
    elif filter_type == 'edge_enhanced_more':
        filtered_image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    else:
        return "Invalid filter type", 400
    
    # Convert filtered image to base64 string
    image_buffer = io.BytesIO()
    filtered_image.save(image_buffer, format='PNG')
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    
    return encoded_image
if __name__ == '__main__':
    app.run(debug=True)
