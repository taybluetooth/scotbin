import pandas as pd
import fitz


GREEN_BIN_COLOR = (93, 187, 94)
GREY_BIN_COLOR = (0, 164, 210)
GREEN = 'green'
GREY = 'grey'


class BinDict:
    def __init__(self, date, color):
        self.date = date
        self.color = color
        self.month = None


def rgb_to_rgb(rgb):
    if len(rgb) != 3:
        raise ValueError("RGB must be a list of four values.")

    R, G, B = rgb
    R = 255 * R
    G = 255 * G
    B = 255 * B
    return int(R), int(G), int(B)


def get_bin_type(shape, color):
    return rgb_to_rgb(shape['fill']) == color


def extract_text_in_shapes(pdf_path):
    doc = fitz.open(pdf_path)
    text_in_shapes = []

    for page in doc:
        shapes = page.get_drawings()
        shapes.sort(key=lambda s: (round(s['rect'].x0 / 5), s['rect'].y0))

        for shape in shapes:
            if shape['fill'] and page.get_textbox(shape['rect']):
                if get_bin_type(shape, GREEN_BIN_COLOR):
                    text_in_shapes.append(BinDict(page.get_textbox(
                        shape['rect']), GREEN))
                elif get_bin_type(shape, GREY_BIN_COLOR):
                    text_in_shapes.append(BinDict(page.get_textbox(
                        shape['rect']), GREY))
    return text_in_shapes


def sort_by_month(data):
    current_month = 1
    sorted_data = []

    for i, current in enumerate(data):
        # Print the current item
        sorted_data.append([f'{current_month}/{current.date}', current.color])

        # Check if there is a next item, then update month if date decreases
        if i < len(data) - 1:  # Make sure there is a next item
            next_item = data[i + 1]
            if current.date > next_item.date:
                current_month += 1

    return sorted_data

def get_bin_calendar(file_path):
    data = extract_text_in_shapes(file_path)
    sorted_data = sort_by_month(data)
    df = pd.DataFrame(sorted_data, columns=['dates', 'colors'])
    json_data = df.set_index('dates')['colors'].to_json()
    return json_data