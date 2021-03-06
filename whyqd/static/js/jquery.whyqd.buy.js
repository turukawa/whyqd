$(document).ready(function() {
    if ($('#stripeButton').length > 0) {
        $.ajax({
            url: $('#stripeSettings').val()
            }).done(function(data) {
                ns = data.settings;
                var handler = StripeCheckout.configure({
                    key: ns.stripe_key,
                    image: '/static/images/qwyre_logo_128pxBW.png',
                    name: ns.novel_title,
                    email: ns.user_email,
                    bitcoin: "true",
                    refund_mispayments: "true",
                    token: function(token) {
                        // http://stackoverflow.com/a/22461608
                        // You can access the token ID with `token.id`
                        if (!ns.user_email) {
                            ns.user_email = token.email;
                        }
                        var is_bitcoin = false;
                        if (token.type === "bitcoin_receiver") {
                            is_bitcoin = true;
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
                                stripeBitcoin: is_bitcoin,
                                template: 'purchase'
                            },
                            success: function(data) {
                                if (data.response == 'success') {
                                    // http://stackoverflow.com/a/8965804
                                    $("#buytrigger").val(true).change();
                                    $('#buynow').empty();
                                    if (data.registered) {
                                        $('#buynow').before(
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
                                    $('#buynowresponse').before(
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
                                $('#buynowresponse').after(
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
                        name: "Whythawk Limited (Qwyre)",
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
        var preorder_text = $('#novelPreorder').attr('value').trim();
        var base_price = parseFloat($('#basePrice').attr('value').trim());
        var next_price = $('#nextPrice').attr('value').trim();
        var select_price = parseFloat($(this).attr('data-value').trim());
        var new_price = (select_price * base_price);
        if (next_price) {
            next_price = (parseFloat(next_price) * select_price/100);
        }
        switch (this.id) {
            case 'forex_usd':
                $('#stripeButton').html(preorder_text + " for $ " + (new_price/100).toFixed(2));
                $("#stripeCurrency").val('USD');
                if (next_price) {
                    $('#nextPriceText').html("Price increases to $ " + next_price.toFixed(2));
                }
                break;
            case 'forex_gbp':
                $('#stripeButton').html(preorder_text + " for &pound; " + (new_price/100).toFixed(2));
                $("#stripeCurrency").val('GBP');
                if (next_price) {
                    $('#nextPriceText').html("Price increases to &pound; " + next_price.toFixed(2));
                }
                break;
            case 'forex_eur':
                $('#stripeButton').html(preorder_text + " for &euro; " + (new_price/100).toFixed(2));
                $("#stripeCurrency").val('EUR');
                if (next_price) {
                    $('#nextPriceText').html("Price increases to &euro; " + next_price.toFixed(2));
                }
                break;
            case 'forex_btc':
                $('#stripeButton').html(preorder_text + " for &#3647; " + (new_price/100).toFixed(4));
                if (next_price) {
                    $('#nextPriceText').html("Price increases to &#3647; " + next_price.toFixed(4));
                }
                // Stripe needs this to be in USD for 10min period conversion rate
                var USD_price = parseFloat($('#forex_usd').attr('data-value').trim());
                new_price = (USD_price * base_price);
                $("#stripeCurrency").val('USD');
                break;
        }
        $("#stripePrice").val(new_price.toFixed());
        e.preventDefault();
    });
    $("#buytrigger").change(function () {
        var next_page = '<a href="' + $('#nextpagelink').val()
            + '" class="btn btn-md btn-read nextchapter pull-right" >Next chapter</a>';
        $('#nextpage').html(next_page);
    });
    if ($('#nextPriceText').length) {
        $('#nextbutton').addClass("two-line");
    }
    if ($('#two-line').length) {
        if ($('#nextbutton').length) {
            $('#nextbutton').addClass("two-line");
        } else {
            $('#two-line').addClass("two-line");
        }
    }
});