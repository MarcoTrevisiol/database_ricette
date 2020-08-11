(function() {
    'use strict';

    angular
        .module('recipes')
        .directive('recQuantita', RecQuantitaDirective);


    function RecQuantitaDirective() {
        var directive = {
            restrict: 'A',
            require: 'ngModel',
            link: linkFunction,
        };
        
        return directive;
        
        
        function linkFunction(scope, element, attr, ngModelCtrl) {
            ngModelCtrl.$parsers.push(fromUser);
            ngModelCtrl.$formatters.push(toUser);
        }
        
        function fromUser(quanto) {
            var number = quanto.match(/^[0-9]*(\.[0-9]*)?/)[0];
            var unitRegex = number + "\(.*\)$";
            var unit = quanto.match(unitRegex)[1];
            var amount = 1;
            if (number.length > 0)
                amount = parseFloat(number);
            return {
                valore: amount,
                unita: unit,
            };
        }

        function toUser(quanto) {
            return quanto.valore.toString() + quanto.unita;
        }
    }
        
})();
