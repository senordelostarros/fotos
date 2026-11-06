"""Como insta.recortar pero conserva TODAS las piezas (kits con accesorios sueltos)."""
import numpy as np
from PIL import Image
from scipy import ndimage
def recortar_todo(path, umbral=238):
    im = Image.open(path).convert("RGB"); a = np.asarray(im).astype(np.int16)
    claro = a.max(axis=2) > umbral
    et, n = ndimage.label(claro)
    borde = set(et[0, :]) | set(et[-1, :]) | set(et[:, 0]) | set(et[:, -1]); borde.discard(0)
    obj = ~np.isin(et, list(borde))
    ys, xs = np.where(obj)
    rgba = im.convert("RGBA"); al = np.where(obj, 255, 0).astype(np.uint8)
    rgba.putalpha(Image.fromarray(al))
    return rgba.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
