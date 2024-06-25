function toggleMore(category) {
    console.log('Toggle more clicked for category:', category);
    var list = document.getElementById('list-' + category);
    if (list) {
        var items = list.getElementsByTagName('li');
        for (var i = 3; i < items.length; i++) {
            items[i].classList.toggle('d-none');
        }
    }
}
