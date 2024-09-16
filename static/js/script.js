let initialHeightHtml = $('html').css('height');
let initialHeightBody = $('body').css('height');

function openModal() {
    $(`#deleteModal`).fadeIn("fast");
    $("html, body").css({ "overflow": 'hidden', "height": '100%' });
}

function closeModal() {
    $(`#deleteModal`).fadeOut("fast");
    $("body").css({ "overflow": 'visible', "height": initialHeightBody });
    $("html").css({ "overflow": 'visible', "height": initialHeightHtml });
}

$('#deleteButton').click(function () {
    openModal();
});

$('#crossButtonModal').click(function () {
    closeModal();
});

$('#cancelButtonModal').click(function () {
    closeModal();
});


$('body').click(function (event) {
    if (!$(event.target).closest('#popup').length && !$(event.target).closest('#deleteButton').length) {
        closeModal();
    }
});
