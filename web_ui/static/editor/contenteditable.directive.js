(function() {
    'use strict';

    angular
        .module('recipes')
        .directive('contenteditable', contenteditable);


    function contenteditable() {
        var directive = {
            require: 'ngModel',
            link: linkFunction,
        };
        
        return directive;
        
        
        function linkFunction(scope, element, attr, ngModelCtrl) {
            // view -> model
            element.on('blur keyup change', function() {
                ngModelCtrl.$setViewValue(element.html());
            });

            // model -> view
            ngModelCtrl.$render = function() {
                element.html(ngModelCtrl.$viewValue);
            };

            // load init value from Model
            ngModelCtrl.$render();
        }
    }
})();
