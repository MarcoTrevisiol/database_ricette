(function() {
    'use strict';

    angular
        .module('recipes')
        .directive('recDuration', RecDurationDirective);

        
    function RecDurationDirective() {
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

        function fromUser(minuti) {
            return moment.duration(minuti, 'minutes').toISOString();
        }

        function toUser(isoString) {
            return moment.duration(isoString).asMinutes();
        }

    }
})();
