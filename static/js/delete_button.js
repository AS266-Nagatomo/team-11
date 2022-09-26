$(document).ready(function() {
	$('.delete-confirm').each(function() {
		var $this = $(this);

		$('button.delete', $this).click(function() {
			$(this).addClass('confirm');
		});

		$('button.yes, button.no', $this).click(function() {
			$('button.delete', $this).removeClass('confirm');
		});
	});
});