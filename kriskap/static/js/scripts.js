// Preview Image
function selectImage() {
  const image_f = document.getElementById("image_f");
  const file_container = document.getElementById("file_container");
  const image_view = file_container.querySelector(".image_view");

  image_f.addEventListener("change", function() {
      const file = this.files[0];
      if (file) {
          const reader = new FileReader();

          reader.addEventListener("load", function() {
              image_view.setAttribute("src", this.result);
          });
          reader.readAsDataURL(file);
      } else {
          image_view.setAttribute("src", "static/img/product_pics/default.png");
      }
  });
}


// Update Cart Section
$(document).ready(function() {
    $('.quantityChange').on('change', function() {
        var cart_id = $(this).attr('cart_id');
        var quantity = $('#quantityChange'+cart_id).val();
        if (quantity < 1) {
            $('#quantityChange'+cart_id).val(1);
            quantity = 1
        }
        if (quantity) {
            req = $.ajax({
                url : '/update',
                type : 'POST',
                data : { cart_id : cart_id, quantity: quantity }
            });
            req.done(function(data) {
                if (quantity > data.max){
                    $('#quantityChange'+cart_id).val(data.max);
                }
                $('#cartNumber'+cart_id).text(data.total);
                $('#cartTotal').text(data.cart_total);
                $('#cart_subtotal').text(data.cart_subtotal);
            });
        }
    });
});


// Update View Product Section
$(document).ready(function() {
    $('#quantity').on('change', function() {
    var quantity = $('#quantity').val();
    var product_id = $('#productId').val();
    req = $.ajax({
        url : '/check-stock',
        type : 'POST',
        data : { quantity: quantity, product_id:product_id }
    });
    req.done(function(data) {
        if (quantity > data.available_stock) {
            $('#quantity').val(data.available_stock);
        }
    });
});
});