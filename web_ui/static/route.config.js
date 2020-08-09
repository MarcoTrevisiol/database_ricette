angular
    .module('recipes')
    .config(['$routeProvider', configRoute]);

function configRoute($routeProvider) {
    $routeProvider
        .when('/editor', {
            templateUrl: 'static/editor_ricetta.html',
            controller: 'Controller',
            controllerAs: 'recipe'
        })
        .otherwise('/editor');
}
