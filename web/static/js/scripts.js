var LANGUAGE_PACKAGE = {
	'usa': {
		'logo': 'Stop Voicies',
		'status': {
			'default': 'Voicies messages is',
			'on': 'Activated',
			'off': 'Deactivated'
		},
		'table': ['Status', 'Date', 'Name', 'Exceptions']
	},
	'rus': {
		'logo': 'ГС блок',
		'status': {
			'default': 'Голосовые сообщения',
			'on': 'Включены',
			'off': 'Выключены'
		},
		'table': ['Статус', 'Дата', 'Имя', 'Ошибки']
	}
};
var NOW_LANG = 'usa';
set_language();
update_lang_image();

document.getElementById('start-btn').onclick = function () {
	var status = document.getElementById('status');
	if (status.classList.contains('activate')) {
		status.classList.remove('activate');
		status.classList.add('deactivate');
		status.innerHTML = LANGUAGE_PACKAGE[NOW_LANG]['status']['off'];

		this.classList.add('pressed');
		this.innerHTML = '<i class="fa-solid fa-microphone-slash"></i>';

		eel.run_voice_blocked(true)(function (answer) {
			alert(answer);
		});
	} else {
		status.classList.remove('deactivate');
		status.classList.add('activate');
		status.innerHTML = LANGUAGE_PACKAGE[NOW_LANG]['status']['on'];

		this.classList.remove('pressed')
		this.innerHTML = '<i class="fa-solid fa-microphone"></i>';

		eel.run_voice_blocked(false)(function (answer) {
			alert(answer);
		});
	}
}

document.getElementById('select-lang-btn').onclick = function () {
	var lang_list = document.getElementById('lang-list-container');
	var status = lang_list.style.display;
	if (status == 'none' || status == '') {
		lang_list.style.display = 'block';
	} else {
		lang_list.style.display = 'none';
	}
}

const langs = document.getElementsByClassName('lang-item');

for (var i = 0; i < langs.length; i++) {
	langs[i].onclick = function () {
		var now_image = document.getElementById('select-lang-btn');
		name = this.getAttribute('name');
		NOW_LANG = name;
		update_lang_image();
		set_language();
	}
}

function update_lang_image() {
	var now_image = document.getElementById('select-lang-btn');
	const image_url = `http://localhost:8000/static/img/${NOW_LANG}_flag.png`;
	now_image.src = image_url;
}

function set_language() {
	const lang_options = LANGUAGE_PACKAGE[NOW_LANG];

	var logo_text = document.getElementById('logo-text');
	logo_text.innerHTML = lang_options['logo'];

	var status_default_text = document.getElementById('status-default-text');
	var status_text = document.getElementById('status');
	status_default_text.innerHTML = lang_options['status']['default'];
	if (status_text.classList.contains('activate')) {
		status_text.innerHTML = lang_options['status']['on'];
	} else {
		status_text.innerHTML = lang_options['status']['off'];
	}

	var table = document.getElementsByClassName('table-text');
	for (var i = 0; i < table.length; i++) {
		table[i].innerHTML = lang_options['table'][i];
	}
}



document.getElementById('update_logs').onclick = function () {
	eel.update_logs()(function (html) {
		document.getElementById('log-table').innerHTML = html;
	});
	set_language();
}