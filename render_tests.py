import subprocess, os
from PIL import Image

base_dir = os.path.abspath('.')
widths = [360, 375, 390]
for width in widths:
    test_html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #faf9f5; display: flex; justify-content: center; }}
  iframe {{ width: {width}px; height: 1800px; border: none; background: #faf9f5; }}
</style>
</head>
<body>
  <iframe id="f" src="index.html"></iframe>
</body>
</html>"""
    html_path = os.path.join(base_dir, f'test_{width}.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    out_img = os.path.join(base_dir, f'{width}_full.png')
    res = subprocess.run([
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--user-data-dir=' + os.path.join(os.environ['TEMP'], f'ch_{width}'),
        '--window-size=600,1800',
        f'--screenshot={out_img}',
        'file:///' + html_path.replace('\\', '/')
    ], capture_output=True, text=True)
    print(f'Width {width} code: {res.returncode}, out: {res.stdout}, err: {res.stderr}')
    
    if os.path.exists(out_img):
        im = Image.open(out_img)
        left = int((600 - width) / 2)
        right = left + width
        crop = im.crop((left, 550, right, 1500))
        crop.save(os.path.join(base_dir, f'{width}_sg_crop.png'))
        print(f'Cropped {width} saved')

print('All done!')
