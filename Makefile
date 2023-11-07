# Use 'make format' to reformat azuracast_xmltv
# Indentation in this file MUST use tabs!

format:
	isort --profile black azuracast_xmltv
	black azuracast_xmltv
