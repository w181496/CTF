var system = require('system');
var args = system.args;
var site = args[1];
var page = require('webpage').create();

page.settings.resourceTimeout = 1000;

function onPageReady() {
    var htmlContent = page.evaluate(function () {
        return document.documentElement.outerHTML;
    });

    console.log(htmlContent);

    phantom.exit();
}


page.open('http://localhost:8080/validator?site=' + site, function (status) {
    function checkReadyState() {
        setTimeout(function () {
            var readyState = page.evaluate(function () {
                return document.readyState;
            });

            if ("complete" === readyState) {
                onPageReady();
            } else {
                checkReadyState();
            }
        });
    }

    checkReadyState();
});
page.onResourceReceived = function(response) {
    console.log("response: " );
};

