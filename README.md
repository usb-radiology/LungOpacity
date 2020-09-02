# LungOpacity

[![DOI](https://zenodo.org/badge/292289868.svg)](https://zenodo.org/badge/latestdoi/292289868)

Following subprojects are included (in the subfolders)
 * lung_mask - lung segmentation using NiftyNet
 * lung_report - lung HU quantification report


## Pre-requistes
To run this pipeline, Linux, Git, Docker, NVIDIA Container Toolkit are needed.


## Build Docker
```shell
docker build -t lung_opacity .
```

### run the code 
```shell
bash run.sh -i input_path_in_nii -o output_path_for_mask_in_nii
```

### Citing LungOpacity
If you use LungOpacity in your work, please cite [Anastasopoulos et al.][EJR109233]

* C. Anastasopoulos, T. Weikert, S. Yang, A. Abdulkadir, L. Schmuelling, C. Buehler, F. Paciolla, R. Sexauer, J. Cyriac, I. Nesic, R. Twerenbold, J. Bremerich, B. Stieltjes, A. W. Sauter, G. Sommer
[Development and clinical implementation of tailored image analysis tools for COVID-19 in the midst of the pandemic: The synergetic effect of an open, clinically embedded software development platform and machine learning][EJR109233] European Journal of Radiology, 2020,109233, ISSN 0720-048X, DOI: [10.1016/j.ejrad.2020.109233][EJR109233]


[EJR109233]: https://doi.org/10.1016/j.ejrad.2020.109233
