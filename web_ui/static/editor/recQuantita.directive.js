(function() {
    'use strict';

    angular
        .module('recipes')
        .directive('recQuantita', RecQuantitaDirective);


    function RecQuantitaDirective() {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function(scope, element, attr, ngModelCtrl) {
                function fromUser(quanto) {
                    number = quanto.match(/^[0-9]*(\.[0-9]*)?/)[0];
                    unitRegex = number + "\(.*\)$";
                    unit = quanto.match(unitRegex)[1];
                    if (number.length > 0)
                        amount = parseFloat(number);
                    else
                        amount = 1;
                    return {
                        valore: amount,
                        unita: unit,
                    };
                }

                function toUser(quanto) {
                    return quanto.valore.toString() + quanto.unita;
                }
                ngModelCtrl.$parsers.push(fromUser);
                ngModelCtrl.$formatters.push(toUser);
            },
        };
    };
})();
