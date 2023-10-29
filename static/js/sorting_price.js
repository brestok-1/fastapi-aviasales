let ascendingOrder = false
$('#price-sort').on('click', function () {
    sortProductsByPrice();
    changeButtonArrow();
});

function sortProductsByPrice() {
    var productList = $('#ticket-list');
    var products = productList.find('.ticket');

    products.sort(function (a, b) {
        var priceA = parseFloat($(a).data('price'));
        var priceB = parseFloat($(b).data('price'));

        if (ascendingOrder) {
            return priceA - priceB;
        } else {
            return priceB - priceA;
        }
    });

    productList.empty().append(products);

    ascendingOrder = !ascendingOrder;
}

function changeButtonArrow() {
    if (ascendingOrder) {
        $('#price-sort').html('Price <i class="fa-solid fa-arrow-down"></i>')
    } else {
        $('#price-sort').html('Price <i class="fa-solid fa-arrow-up"></i>')
    }
}

