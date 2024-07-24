from PIL import Image

def resize_image(input_image_path, output_image_path, target_width, target_height):
    original_image = Image.open(input_image_path)
    
    # 使用 LANCZOS 濾波器進行 resize，以避免鋸齒狀邊緣
    resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
    
    # 儲存新圖像
    resized_image.save(output_image_path)

if __name__ == '__main__':
    input_path = './rich_menus/images/raw/c2s5.png'  # 替換為你的輸入圖像路徑
    output_path = './rich_menus/images/sz2400x843/c2s5.png'  # 替換為你的輸出圖像路徑
    target_width = 2500  # 目標寬度
    target_height = 843  # 目標高度

    resize_image(input_path, output_path, target_width, target_height)

