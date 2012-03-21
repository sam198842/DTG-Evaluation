
YUI().use('node', 'event', 'dd-drag', 'dd-drop', 'dd-proxy', 'dd-constrain', 'dd-scroll', 'io-form', 'io-base', function (Y) {


	/*
	var tag_groups = {};
	Y.all('.all_unique_tags').on('click', function (e) {
		var node = e.target;
		var tag = node.getContent();
		tag_groups[tag] = (tag_groups[tag] + 1) % COLORS.length;
		var color = COLORS[tag_groups[tag]];
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
	*/

	// Get list of li's in lists and make them draggable
	var lis = Y.all('#group ul li').each(function(v, k) {
		var dd = new Y.DD.Drag({
			node: v,
			target: {
				padding: '0 0 0 20'
			}
		}).plug(Y.Plugin.DDProxy, {
			moveOnEnd: false
		}).plug(Y.Plugin.DDConstrained, {
			constrain2node: '#group'
		}).plug(Y.Plugin.DDNodeScroll, {
			node: v.get('parentNode')
		});
	});

	// Create simple targets for lists
	var uls = Y.all('#group ul').each(function(v, k) {
		var tar = new Y.DD.Drop({
			node: v
		});
	});

	// Static Vars
	var goingUp = false, lastY = 0;

	// Drag Events
	Y.DD.DDM.on('drag:start', function(e) {
		var drag = e.target;
		drag.get('node').setStyle('opacity', '.25');
		drag.get('dragNode').set('innerHTML', drag.get('node').get('innerHTML'));
		drag.get('dragNode').setStyles({
			opacity: '.5',
			borderColor: drag.get('node').getStyle('borderColor'),
			backgroundColor: drag.get('node').getStyle('backgroundColor')
		});
	});

	Y.DD.DDM.on('drag:end', function(e) {
		var drag = e.target;
		drag.get('node').setStyles({
			visibility: '',
			opacity: '1'
		});
	});
	
	Y.DD.DDM.on('drag:drag', function(e) {
	  //Get the last y point
		var y = e.target.lastXY[1];
		//is it greater than the lastY var?
		if (y < lastY) {
			//We are going up
			goingUp = true;
		} else {
			//We are going down.
			goingUp = false;
		}
		//Cache for next check
		lastY = y;
		Y.DD.DDM.syncActiveShims(true);
	});
	
	Y.DD.DDM.on('drop:over', function(e) {
    //Get a reference to our drag and drop nodes
    var drag = e.drag.get('node'),
      	drop = e.drop.get('node');
    //Are we dropping on a li node?
    if (drop.get('tagName').toLowerCase() === 'li') {
      //Are we not going up?
      if (!goingUp) {
        drop = drop.get('nextSibling');
      }
      //Add the node to this list
      e.drop.get('node').get('parentNode').insertBefore(drag, drop);
			//Set the new parentScroll on the nodescroll plugin
			e.drag.nodescroll.set('parentScroll', e.drop.get('node').get('parentNode'));
      //Resize this nodes shim, so we can drop on it later.
      e.drop.sizeShim();
    }
	});

	Y.DD.DDM.on('drag:drophit', function(e) {
    var drop = e.drop.get('node'),
        drag = e.drag.get('node');
    //if we are not on an li, we must have been dropped on a ul
    if (drop.get('tagName').toLowerCase() !== 'li') {
      if (!drop.contains(drag)) {
        drop.appendChild(drag);
				//Set the new parentScroll on the nodescroll plugin
				e.drag.nodescroll.set('parentScroll', e.drop.get('node'));
      }
    }
	});

	// colors used to group tags
	//var COLORS = ['CornflowerBlue', 'Violet', 'Salmon', 'MediumSeaGreen', 'DarkGray'];	
	var COLORS = ['RoyalBlue', 'ForestGreen', 'Red', 'Gold', 'purple'];

	// confirm button handler
	Y.one('#confirm').on('click', function(e) {
		//alert('Hello world');
		var id = 0;
		var groups = new Array();
		Y.all('#group ul').each(function(node) {
			//console.log(node.get('children').size());
			if (node.get('children').size() != 0) {
				node.get('children').each(function(n) {
					groups.push(n.getContent() + '=' + id);
					// set the tags' color by groups
					Y.all('#rank .' + n.getContent() + '').each(
						function (node) {
						node.setStyle('backgroundColor', COLORS[id]);
					});
				});
				id++;
			}
		});
		console.log(groups.join('&'));
		postData = groups.join('&');
		Y.one('#suggestions').show();
	});

	// AJAX POST complete handler
	function complete_handler(id, o) {
		console.log(o);
		alert("Data submitted, click 'OK' to continue.");
		document.location = '.';
	};

	// Data in POST (besides the form)
	var postData;

	var cfg = {
		method: 'POST',
		data: 'password=AAAAA',
		form: {
			id: 'votes'
		},
		on: {
			complete: complete_handler
		}
	};

	// submit button handler
	Y.one('#votes').on('submit', function(e) {
		e.preventDefault();
		cfg.data = postData;
		var submit = false;
		Y.all('.vote').each(function(node) {
			if (node.get('checked'))
				submit = true;
		});
		if (submit)
			Y.io('.', cfg);
		else
			alert('Please make a choice.');
	});

});


