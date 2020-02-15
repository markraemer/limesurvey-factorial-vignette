<script type="text/javascript" charset="utf-8">
	$(document).on('ready pjax:scriptcomplete',function(){
		var thisQuestion = $('#question{QID}');

		{% for sq in data %}
		// Insert selects
		$('.answer_cell_{{data[sq].id}}', thisQuestion).append('<select class="inserted-select form-control list-question-select">\
<option value="">Please choose...</option>\
{% for o in data[sq].options %} <option value="{{loop.index}}">{{o}}</option>\
{% endfor %}</select>');

		// Listeners
		$('.inserted-select', thisQuestion).on('change', function(i) {
			if($(this).val() != '') {
				$(this).closest('.answer_cell_{{data[sq].id}}').find('input:text').val($.trim($('option:selected', this).text())).trigger('change');
			}
			else {
				$(this).closest('.answer_cell_{{data[sq].id}}').find('input:text').val('').trigger('change');
			}
		});

		// Returning to page
		$('input:text', thisQuestion).each(function(i) {
			var thisCell = $(this).closest('.answer_cell_{{data[sq].id}}');
			var inputText = $.trim($(this).val());
			var selectval = $('select.inserted-select option', thisCell).filter(function () { return $(this).html() == inputText; }).val();
			$('select.inserted-select', thisCell).val(selectval);
		});

		$('input[id*=_{{data[sq].id}}]', thisQuestion).css({
			'position': 'absolute',
			'left': '-9999em'
		});

		{% endfor %}

		// Clean-up styles
		$('select.inserted-select', thisQuestion).css({
			'max-width': '100%'
		});

		$('col.answertext').css({
			'width': '5%'
		});

	});
</script>
