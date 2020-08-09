angular
    .module('recipes')
    .directive('recDuration', RecDurationDirective)

function RecDurationDirective() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attr, ngModelCtrl) {
            function fromUser(minuti) {
                return moment.duration(minuti, 'minutes').toISOString();
            }

            function toUser(isoString) {
                return moment.duration(isoString).asMinutes();
            }
            ngModelCtrl.$parsers.push(fromUser);
            ngModelCtrl.$formatters.push(toUser);
        },
    };
};
