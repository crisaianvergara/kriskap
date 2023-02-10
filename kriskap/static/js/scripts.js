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


// Update Cart Quantity
$(document).ready(function() {

    $('.quantityChange').on('change', function() {

        var cart_id = $(this).attr('cart_id');
        var quantity = $('#quantityChange'+cart_id).val();

        if (quantity) {

            req = $.ajax({
                url : '/update',
                type : 'POST',
                data : { cart_id : cart_id, quantity: quantity }
            });
    
            req.done(function(data) {
                $('#cartNumber'+cart_id).text(data.total);
                $('#cartTotal').text(data.cart_total);
                $('#cart_subtotal').text(data.cart_subtotal);
            });
        }



    });

});
