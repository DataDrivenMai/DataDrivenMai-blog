# Font Awesome Icon Plotting

This project demonstrates how to use [Font Awesome icons](https://fontawesome.com/) in Python `matplotlib` figures as text objects or scatter plot paths, including partial icons, custom alignment, and image overlays.

## Blog Post
[Read the full tutorial here](https://www.DataDrivenMai.com/blog/python-matplotlib-font-awesome-icons/)

## Project Structure
- `README.md` (you are here)
- `python-matplotlib-font-awesome-icons.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `python-matplotlib-font-awesome-icons.py`
    - Python script containing only the essential code from the tutorial with minimal explanation
- `data/`
- `images/`

## The Ins and Outs

### Input 
- Unicode identifier of the icons to be used
    - Code will run with default icons in script

### Output
-  Generates figures demonstrating various features possible when plotting Font Awesome icons as text or path objects

## Project Value

### Motivation
Expand your data visualization skills with the power to draw [Font Awesome icons ](https://fontawesome.com/) in your `matplotlib` figures.

### Key Skills Demonstrated
- Display Font Awesome icons as text objects with `matplotlib.pyplot.text()` 
- Draw the icons as path objects with `matplotlib.pyplot.scatter()` 
- Be able to adjust the icon's
    - positioning and alignment
    - size
    - color (face and edge)
    - rotation
- Draw just part of an icon using bounding boxes created with `matplotlib.transforms.Bbox.from_extents()` and clipping the path using the `.clip_to_bbox()` method
- Add image overlays to the icon shape using `set_clip_path()` 

## How to Run
Open the `python-matplotlib-font-awesome-icons.ipynb` notebook and run all cells sequentially, or run the `python-matplotlib-font-awesome-icons.py` python script in one go.

### Requirements for Code to Run
- Python 3 (Verified on 3.14.3)
- Python libraries
	- `numpy`
	- `matplotlib.font_manager`
    - `matplotlib.pyplot`
	- `matplotlib.textpath`
	- `matplotlib.transforms`
	- `matplotlib.path`
	- `matplotlib.patches`
    - `matplotlib.gridspec` (just for python-matplotlib-font-awesome-icons.py) 
    - `Pillow`
- `data/` subfolder with 
    - Font Awesome OTF files
    - Flag images for the image overlay demonstration
