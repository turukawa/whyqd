$(document).ready(function() {
    if ($('#stripeButton').length > 0) {
        $.ajax({
            url: $('#stripeSettings').val()
            }).done(function(data) {
                ns = data.settings;
                var handler = StripeCheckout.configure({
                    key: ns.stripe_key,
                    image: '/media/images/qwyre_42.png',
                    name: ns.novel_title,
                    email: ns.user_email,
                    token: function(token) {
                        // http://stackoverflow.com/a/22461608
                        // You can access the token ID with `token.id`
                        if (!ns.user_email) {
                            ns.user_email = token.email;
                        }
                        $.ajax({
                            url: $('#stripeBuy').val(),
                            type: 'post',
                            data: {
                                stripeToken: token.id,
                                stripeDescription: ns.description,
                                stripePrice: ns.price,
                                stripeCurrency: ns.currency,
                                stripeEmails: ns.user_email,
                                selfPurchase: true, // Buying for own use
                                template: 'purchase'
                            },
                            success: function(data) {
                                if (data.response == 'success') {
                                    // http://stackoverflow.com/a/8965804
                                    $("#buytrigger").val(true).change();
                                    $('#buynow').empty();
                                    if (data.registered) {
                                        $('#buynow').after(
                                            '<div class="alert alert-success alert-dismissable">'+
                                            '<button type="button" class="close" ' + 
                                            'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                            '</button>' + 
                                            '<p><strong>Thank you</strong>, your purchase has been successful.</p>' +
                                            '<p>You can continue reading ' + ns.novel_title + ' online, or ' +
                                            '<a href="' + data.link + '" class="alert-link"> download an ebook ' +
                                            'version</a>. You could even share a copy with your friends.</p>' +
                                            '</div>');
                                    }
                                    else {
                                        // http://stackoverflow.com/a/506004
                                        window.location.href = data.link;
                                    }
                                }
                                else {
                                    $('#buynow').after(
                                        '<div class="alert alert-danger alert-dismissable">'+
                                            '<button type="button" class="close" ' + 
                                                'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                            '</button>' + 
                                            '<strong>Sorry</strong>, something went wrong. ' +
                                            'You have not been charged. Please try again.' +
                                         '</div>');
                                }
                            },
                            error: function(data) {
                                $('#buynow').after(
                                    '<div class="alert alert-danger alert-dismissable">'+
                                        '<button type="button" class="close" ' + 
                                            'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                        '</button>' + 
                                        '<strong>Sorry</strong>, something went wrong. ' +
                                        'You have not been charged. Please try again.' +
                                     '</div>');
                            }
                          }); // end ajax call
                    }
                });
                document.getElementById('stripeButton').addEventListener('click', function(e) {
                    ns.price = $('#stripePrice').val().trim();
                    ns.description = "Single purchase of " + ns.novel_title;
                    ns.currency = $('#stripeCurrency').val();
                    // Open Checkout with further options
                    handler.open({
                      description: ns.description,
                      amount: ns.price,
                      currency: ns.currency
                    });
                    e.preventDefault();
                });
            });
    }
    $('[id^=forex_]').on('click', function (e) {
        var forex = this;
        var base_price = parseFloat($('#basePrice').attr('value').trim()).toFixed(2);
        var next_price = $('#nextPrice').attr('value').trim();
        var select_price = parseFloat($(this).attr('data-value').trim()).toFixed(2);
        console.log(base_price);
        console.log($('#'+this.id).val());
        var new_price = (select_price * base_price);
        if (next_price) {
            next_price = (parseFloat(next_price).toFixed(2) * select_price/100).toFixed(2);
        }
        $("#stripePrice").val(new_price.toFixed());
        switch (this.id) {
            case 'forex_usd':
                $('#stripeButton').html("Buy for $ " + (new_price/100).toFixed(2));
                $("#stripeCurrency").val('USD');
                if (next_price) {
                    $('#nextPriceText').html("Price increases to $ " + next_price);
                }
                break;
            case 'forex_gbp':
                $('#stripeButton').html("Buy for &pound; " + (new_price/100).toFixed(2));
                $("#stripeCurrency").val('GBP');
                if (next_price) {
                    $('#nextPriceText').html("Price increases to &pound; " + next_price);
                }
                break;
            case 'forex_eur':
                $('#stripeButton').html("Buy for &euro; " + (new_price/100).toFixed(2));
                $("#stripeCurrency").val('EUR');
                if (next_price) {
                    $('#nextPriceText').html("Price increases to &euro; " + next_price);
                }
                break;
        }
        e.preventDefault();
    });
});