

YUI().use('node', 'event', 'dd-drag', function (Y) {

	var dd = new Y.DD.Drag({
			node: '#demo'
	});

	var tag_group = {};
	var COLORS = ['red','yellow', 'blue', 'green', 'purple'];

	Y.all('.all_unique_tags').on('click', function (e) {
		var node = e.target;
		var tag = node.getContent();
		tag_group[tag] = (tag_group[tag] + 1) % COLORS.length;
		var color = COLORS[tag_group[tag]];
		node.setStyle('backgroundColor', color);
		Y.all('.' + tag).each(
			function (node) {
				node.setStyle('backgroundColor', color);
			}
		);
	});

	Y.one('window').on('load', function(e) {
		Y.all('.all_unique_tags').each(
			function (node) {
				tag_group[node.getContent()] = -1
			}
		);
		console.log(tag_group);
	});

});

function checkForm(form) {
	alert(document.getElementById('id_pop').checked);
	return false;
}

