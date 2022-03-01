# -*- coding: utf-8 -*-

import eel
import stopvoice
from jinja2 import Template

eel.init('web')


@eel.expose
def run_voice_blocked(status):
	if status:
		stopvoice.connect()
	else:
		stopvoice.disconnect()
	return status


@eel.expose
def update_logs():
	with open('web/layouts/log_table.html') as html_file:
		context = {'logs': stopvoice.log_list}
		template = Template(html_file.read())
		# return stopvoice.log_list
		html = template.render(**context)

		return html


def main():
	eel.start('index.html')


if __name__ == '__main__':
	main()