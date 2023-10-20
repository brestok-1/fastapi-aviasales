let ascendingOrderCount = true
$('#quanity-sort').on('click', function () {
    sortProductsByQuantity();
    changeButtonArrowQuantity();
});

function sortProductsByQuantity() {
    var productList = $('#ticket-list');
    var products = productList.find('.ticket');

    products.sort(function (a, b) {
        var priceA = parseFloat($(a).data('count'));
        var priceB = parseFloat($(b).data('count'));

        if (ascendingOrderCount) {
            return priceA - priceB;
        } else {
            return priceB - priceA;
        }
    });

    productList.empty().append(products);

    ascendingOrderCount = !ascendingOrderCount;
}

function changeButtonArrowQuantity() {
    if (ascendingOrderCount) {
        $('#quanity-sort').html('Quantity <i class="fa-solid fa-arrow-down"></i>')
    } else {
        $('#quanity-sort').html('Quantity <i class="fa-solid fa-arrow-up"></i>')
    }
}
