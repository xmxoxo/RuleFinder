function Table() {
	var TClass = {};
	var Tool = {};
	var DataStore = {};
	var Option = {};
	Tool.createHeader = function(htmls, data) {
		htmls.push('<tr>');
		for (var i in data) {
			htmls.push('<th>' + data[i] + '</th>');
		}
		htmls.push('</tr>');
	};
	Tool.createRow = function(htmls, data) {
		htmls.push('<tr>');
		for (var i in data) {
			htmls.push('<td>' + data[i] + '</td>');
		}
		htmls.push('</tr>');
	};
	Tool.render = function(id, tag) {
		var htmls = [];
		var option = Option[id];
		if (option['title'] != null) {
			htmls.push('<div class="title">' + option['title'] + '</div>');
		}
		htmls.push('<table>');
		Tool.createHeader(htmls, DataStore[id]['header']);
		for (var i in DataStore[id]['data']) {
			Tool.createRow(htmls, DataStore[id]['data'][i]);
		}
		htmls.push('</table>');
		tag.empty().append(htmls.join(''));
		Tool.setStyle(id, tag);
	};
	Tool.setStyle = function(id, tag) {
		var option = Option[id];
		tag.find('.title').css({
			'font-weight': 'bold',
			'text-align': 'center',
			'color': option['titleColor'],
			'font-size': option['titleSize']
		});
		tag.find('table').css({
			'width': '100%'
		});
		tag.find('th').css({
			'color': option['headerColor'],
			'background-color': option['headerBgColor'],
			'font-size': option['headerSize']
		});
		tag.find('tr td').css({
			'color': option['color'],
			'font-size': option['size'],
			'text-align': option['align'],
		});
		tag.find('tr:even td').css({
			'background-color': option['evenBgColor']
		});
		tag.find('tr:odd td').css({
			'background-color': option['oddBgColor']
		});
		if (option['rowHeight'] != null) {
			tag.find('tr').find('th:eq(0)').css('height', option['rowHeight']);
			tag.find('tr').find('td:eq(0)').css('height', option['rowHeight']);
		}
		if (option['columnWidth'] != null) {
			var td = tag.find('tr').find('th');
			$.each(td,
			function(i) {
				$(this).css('width', option['columnWidth'][i] + '%');
			});
		}
	};
	Tool.getValue = function(value, defalutValue) {
		if (typeof value == 'undefined') {
			return defalutValue;
		} else {
			return value;
		}
	};
	TClass.init = function(option) {
		var id = option['id'];
		var tag = $('#' + id);
		var header = option['header'];
		var data = option['data'];
		DataStore[id] = {
			header: header,
			data: data
		};
		Option[id] = {
			title: Tool.getValue(option['title'], null),
			titleColor: Tool.getValue(option['titleColor'], 'black'),
			titleSize: Tool.getValue(option['titleSize'], 14),
			headerColor: Tool.getValue(option['headerColor'], 'black'),
			headerBgColor: Tool.getValue(option['headerBgColor'], '#A2FD9A'),
			headerSize: Tool.getValue(option['headerSize'], 14),
			color: Tool.getValue(option['color'], 'black'),
			size: Tool.getValue(option['size'], 14),
			align: Tool.getValue(option['align'], 'left'),
			evenBgColor: Tool.getValue(option['evenBgColor'], '#E3F4FD'),
			oddBgColor: Tool.getValue(option['oddBgColor'], '#FDF0E6'),
			rowHeight: Tool.getValue(option['rowHeight'], 34),
			columnWidth: Tool.getValue(option['columnWidth'], null)
		};
		Tool.render(id, tag);
	};
	TClass.getValue = function(id, row, column) {
		return DataStore[id]['data'][row - 1][column - 1];
	};
	TClass.setValue = function(id, row, column, value) {
		DataStore[id]['data'][row - 1][column - 1] = value;
	};
	TClass.getValues = function(id) {
		return DataStore[id]['data'];
	};
	TClass.addRow = function(id, data) {
		DataStore[id]['data'].push(data);
	};
	TClass.deleteRow = function(id, row) {
		DataStore[id]['data'].splice(row - 1, 1);
	};
	TClass.getRowCount = function(id) {
		return DataStore[id]['data'].length;
	};
	TClass.render = function(id) {
		Tool.render(id, $('#' + id));
	};
	return TClass;
}