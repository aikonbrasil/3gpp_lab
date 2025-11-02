for i in *.docx
do
	echo item: $i

	libreoffice --headless --convert-to pdf $i
done