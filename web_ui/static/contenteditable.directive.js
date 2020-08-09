angular
    .module('recipes')
    .directive('contenteditable', contenteditable)


function contenteditable() {
    return {
        require: 'ngModel',
        link: function(scope, element, attr, ngModelCtrl) {
            // view -> model
            element.on('blur', function() {
                ngModelCtrl.$setViewValue(element.html());
            });

            // model -> view
            ngModelCtrl.$render = function() {
                element.html(ngModelCtrl.$viewValue);
            };

            // load init value from Model
            ngModelCtrl.$render();
        }
    };
};
