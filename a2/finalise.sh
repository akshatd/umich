#!/usr/bin/env bash

final_pdf='akshatdy_AE588_A1.pdf'
all_pdfs=()
appendix=()

# convert to python scripts
nb_list=($(ls ./*.ipynb))
jupyter nbconvert --to script ${nb_list[@]}

# format with pep8
py_list=($(ls ./*.py))
autopep8 --verbose --in-place --aggressive --aggressive ${py_list[@]}

nb_pdfs=()
# convert to pdf
for nb in ./*.ipynb; do
	jupyter nbconvert --to html $nb
	wkhtmltopdf ${nb/ipynb/html} ${nb/ipynb/pdf}
	rm -v ${nb/ipynb/html}
	nb_pdfs+=(${nb/ipynb/pdf})
done

# add additional all_all_pdfs
all_pdfs+=(${nb_pdfs[@]})
all_pdfs+=(${appendix[@]})

# combine all_pdfs
pdfunite ${all_pdfs[@]} $final_pdf

# remove intermediate notebook pdfs
rm -v ${nb_pdfs[@]}
