angular
    .module('recipes')
    .config(['$routeProvider', configRoute]);

function configRoute($routeProvider) {
    $routeProvider
        .when('/nuova_ricetta', {
            templateUrl: 'static/new_recipe/new_recipe.html',
            controller: 'NewRecipeController',
            controllerAs: 'vm'
        })
        .otherwise('/nuova_ricetta');
}
