"""GIMP MCP filters pack - sharpen, emboss, brightness/contrast."""
import subprocess
import tempfile
import os


def run_gimp_script(script):
    """Run a GIMP Script-Fu script."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.scm', delete=False) as f:
        f.write(script)
        script_path = f.name
    try:
        result = subprocess.run(
            ['gimp', '-i', '-b', f'(load "{script_path}")'],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    finally:
        os.unlink(script_path)


def sharpen(image_path, radius=1.0, amount=1.0):
    """Apply sharpen filter."""
    script = f"""
    (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE "{image_path}" "{image_path}")))
           (drawable (car (gimp-image-flatten image))))
      (plug-in-unsharp-mask RUN-NONINTERACTIVE image drawable {radius} {amount} 0)
      (gimp-file-save RUN-NONINTERACTIVE image drawable "{image_path}" "{image_path}")
      (gimp-image-delete image))
    """
    return run_gimp_script(script)


def emboss(image_path, azimuth=135, elevation=45, depth=3):
    """Apply emboss filter."""
    script = f"""
    (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE "{image_path}" "{image_path}")))
           (drawable (car (gimp-image-flatten image))))
      (plug-in-emboss RUN-NONINTERACTIVE image drawable {azimuth} {elevation} {depth} 1)
      (gimp-file-save RUN-NONINTERACTIVE image drawable "{image_path}" "{image_path}")
      (gimp-image-delete image))
    """
    return run_gimp_script(script)


def brightness_contrast(image_path, brightness=0, contrast=0):
    """Apply brightness/contrast adjustment."""
    script = f"""
    (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE "{image_path}" "{image_path}")))
           (drawable (car (gimp-image-flatten image))))
      (gimp-brightness-contrast drawable {brightness} {contrast})
      (gimp-file-save RUN-NONINTERACTIVE image drawable "{image_path}" "{image_path}")
      (gimp-image-delete image))
    """
    return run_gimp_script(script)
