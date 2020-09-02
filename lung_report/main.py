import argparse
import io
import json
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer

import imgkit
import numpy as np
import pandas as pd
from environs import Env
from jinja2 import Environment, FileSystemLoader, select_autoescape

from hu_ranges import get_hu_ranges
from processing import create_images

import os 

dirname = os.path.dirname(__file__)
template_dir = os.path.join(dirname, 'templates')

print(template_dir)

env = Env()
env.read_env()  # read .env file, if it exists
templates_path = env("TEMPLATES_PATH", template_dir)

env = Environment(
    loader=FileSystemLoader(templates_path),
    autoescape=select_autoescape(["html", "xml"]),
)


def to_date(date_as_int):
    if date_as_int:
        return datetime.strptime(str(date_as_int), "%Y%m%d").strftime("%d.%m.%Y")
    else:
        return ""


def now():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


env.filters["to_date"] = to_date
env.globals["now"] = now

version = "0.4"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="image", required=True, help="Image path")
    parser.add_argument("-m", dest="mask", required=True, help="Mask path")
    parser.add_argument("-o", dest="output_dir", required=True, help="Output folder")
    parser.add_argument("--version", action="version", version=f"{version}")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    print(f"Saving outputs to dir: {output_dir}")


    if (Path(args.image).parent.parent / "nodeinfo.json").exists():
        with open(Path(args.image).parent.parent / "nodeinfo.json", "r") as f:
            metadata = json.load(f)
    else:
        metadata = {
             "PatientName": "Unknown",
             "PatientSex": "Unknown",
             "PatientBirthDate": "19000101",
             "PatientID": "Unknown",
             "StudyID": "Unknown",
             "StudyDescription": "Unknown",
             "StudyDate": "19000101",
        }

    start = timer()
    images, (hu_values, bins), pixdim_prod = create_images(
        args.image, args.mask, output_dir
    )
    end = timer()
    print(f"Image creation took: {(end-start):.3f} sec")
    lung_ml = abs(int(round(np.sum(bins) * pixdim_prod / 1000)))
    hu600_0 = (
        abs(int(round(np.sum(bins[4:]) * pixdim_prod / 1000))),
        np.sum(hu_values[4:]),
    )
    hu200_0 = (
        abs(int(round(np.sum(bins[8:]) * pixdim_prod / 1000))),
        np.sum(hu_values[8:]),
    )

    hu_range_text = lambda x: str(x).replace(" ", "").replace(",", "_")
    pd.DataFrame(
        {
            "hu_range": list(map(hu_range_text, get_hu_ranges())),
            "percentage": hu_values,
            "total": bins,
        }
    ).to_json(f"{output_dir}/hu_summary.json")

    start = timer()
    t = env.get_template("template.html")
    output_html = t.render(
        version=version,
        images=images,
        hu_values=hu_values,
        lung_ml=lung_ml,
        hu600_0=hu600_0,
        hu200_0=hu200_0,
        metadata=metadata,
    )
    end = timer()
    print(f"HTML template creation took: {(end-start):.3f} sec")

    options = {"xvfb": "", "format": "png", "width": "2400", "height": "1200"}

    print("Start generating screenshot ...")
    report_file = output_dir / "report.png"
    imgkit.from_string(output_html, str(report_file), options=options)
    print(f"Screenshot saved to {report_file}")
    # delete images for report, nobody cares
    for i in images:
        Path(i).unlink()
    # We are not returning anything because everything in the output folder will be added by nora (see bash script)
    return 0


if __name__ == "__main__":
    main()
